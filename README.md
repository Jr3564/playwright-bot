## Installation

- Create the virtual environment

  ```bash
    virtualenv -p python3 venv
  ```

- Activate environment 

  ```bash
    source venv/bin/activate
  ```

- Install the requirements

  ```bash
  pip install -r requirements.txt
  ```

- Install playwright requirements

  ```bash
  playwright install
  ```

  - If that doesn't work, the following command will install the required dependencies:

    ```bash
    playwright install-deps
    ```



## Required input files examples



#### .env file

```.env
EMAIL=email@email.com
PASSWORD=senha123
```

#### CSV file

```csv
email
https://www.linkedin.com/in/profile1/
https://www.linkedin.com/in/profile2/
https://www.linkedin.com/in/profile3/
https://www.linkedin.com/in/profile4/
```



## Running

- To let's start, you need a `.env` file with the credentials in the root folder (in the same folder as main.py).
- After that, just run the main.py, passing as an argument, the absolute path of the `csv` file with the profiles.

```shell
python main.py <file-path>
```

- example

  ```
  python main.py ./profiles.csv
  ```

