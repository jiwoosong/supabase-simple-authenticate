# supabase-simple-authenticate
simple authenticate example with custom supabase database

## installation

```bash
$ pip install git+https://github.com/jiwoosong/supabase-simple-authenticate.git@v0.0.1
```

### Supabase Setting
1. Login to [Supabase](https://supabase.com/)
2. Generate **Project** and activate **RLS**
   ```sql
   ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;
   ```
3. Generate **Database** with setting below

   | Column Name   | Data Type   | Constraints | Description |
   |--------------|------------|-------------|-------------|
   | `id`         | `int8` | Primary Key, Auto Increment | 고유 ID (자동 증가) |
   | `computer_id` | `text` | NOT NULL | 컴퓨터 식별자 |
   | `license`    | `float8` | DEFAULT 0.0 | 라이선스 정보 (버전, 권한 등) |
   | `created_at` | `timestamp` | DEFAULT now() | 생성 시각 (자동 기록) |
   | `updated_at` | `timestamp` | DEFAULT now() | 업데이트 시각 (자동 기록) |
   | `request_n`  | `int8` | DEFAULT 0 | 요청 횟수 (사용량 트래킹) |
   | `extra_data` | `jsonb` | NULLABLE | 추가 데이터 (JSON 형식) |

4. Generate **Policy** with setting below
   > ⚠️ Note: This is just example and vulnerable setting. Select appropriate policy with your purpose.
   * Access Policy Example : Everyone can access.
       ```sql
       alter policy "Access"
       on "public"."YOUR-DATABASE-NAME"
       to public
       using (true);
       ```
   * Insert Policy Example : Anon-user can insert new column.
       ```sql
       alter policy "Insert"
       on "public"."YOUR-DATABASE-NAME"
       to public
       with check (auth.role() = 'anon'::text);
       ```
   * Update Policy Example : Anon-user can update own column. Especial `computer-id` is equal to `CURRENT_USER`.
       ```sql
       alter policy "Update"
       on "public"."YOUR-DATABASE-NAME"
       to public
       using (computer_id = CURRENT_USER)
       with check (
       (computer_id = CURRENT_USER) 
       AND (request_n IS NOT NULL) 
       AND (updated_at IS NOT NULL)
       );
       ```
     Also You can limit especial column update to anon-user by setting `CHECK` option.
       ```sql
       ALTER POLICY "Update"
       ON "public"."YOUR-DATABASE-NAME"
       TO public
       USING (computer_id = CURRENT_USER)
       WITH CHECK (
           (computer_id = CURRENT_USER)
           AND (NEW.request_n IS NOT NULL) 
           AND (NEW.updated_at IS NOT NULL)
           AND (NEW.computer_id = OLD.computer_id) -- Fix this column 
           AND (NEW.extra_data = OLD.extra_data) -- Fix this column
       );
       ```

## Usage

```python
import SupaSimpleAuth
# You can find these information in supabase project API-doc.
URL = r'https://YOUR-SUPABASE-PROJECT-URL.supabase.co'
DB_Name = r'YOUR-SUPABASE-DATABASE/TABLE-NAME'
API_KEY = r'YOUR-SUPABASE-API-KEY'
JWT = r'YOUR-SUPABASE-JWT'
```
* First Time (Registration)
   ```python
   >>> SupaSimpleAuth.client.client_requestclient_request(URL, DB_Name, API_KEY, JWT, init_license=1.0, init_extra_data=None)
   {'status': 'success',
    'message': '신규 라이선스 등록 완료 (computer_id=YOUR-DESKTOP-NAME)',
    'data': {'computer_id': 'YOUR-DESKTOP-NAME',
             'license': 1.0,
             'request_n': 1,
             'created_at': 'CURRENT-DATE',
             'updated_at': 'UPDATED-DATE', 'extra_data': {}}}
   ```
* Second Time
   ```python
    >>> SupaSimpleAuth.client.client_requestclient_request(URL, DB_Name, API_KEY, JWT, init_license=1.0, init_extra_data=None)
   {'status': 'success',
    'message': '조회 횟수 업데이트 완료: 2회',
    'data': {'computer_id': 'YOUR-DESKTOP-NAME',
             'license': 1.0,
             'request_n': 2,
             'created_at': 'CURRENT-DATE',
             'updated_at': 'UPDATED-DATE',
             'extra_data': {}
             }
    }
   ```