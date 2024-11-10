# datagen

datagen is a Python package that generate data to MySQL Database directly.

When you need data for MySQL for some reasons (for test), and too lazy to make mock data, here is the answer.  

## Usage

```bash
pip install datagen
```

import datagen

conn = datagen.mysql_connect(
    host = 
    port =
    user = 
    password =
    db = 
)

datagen.generate(
    conn: conn
    table: str (테이블 명)
    cnt: int (횟수)
    
    col1 = uuid
    col2 = name
    time = 1 (어제, 0은 오늘)
    
    pk 처리 해야함? -> pk면 모든 
    **kwargs
)
