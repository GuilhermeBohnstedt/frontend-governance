# Frontend Governance Monorepo

This repository contains both the backend (FastAPI) and frontend (SvelteKit) for the Frontend Governance project.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Backend](#backend)
- [Frontend](#frontend)
- [Additional Notes](#additional-notes)
- [Running Tests](#running-tests)
- [License](#license)

---

## Project Structure

```
frontend-governance/
├── backend/         # FastAPI backend application
│   ├── main.py
│   ├── requirements.txt
│   ├── venv/
│   └── tests.py
├── frontend/        # SvelteKit frontend application
│   ├── src/
│   ├── package.json
│   └── pnpm-lock.yaml
├── README.md
└── ...
```

## Backend

To set up and run the backend server, follow these steps:

1. **Navigate to the backend directory:**

```bash
cd ./backend
```

2. **Activate the Python virtual environment:**

```bash
source venv/bin/activate
```

3. **Install the required Python packages:**

```bash
pip install -r backend/requirements.txt
```

4. **Start the backend server using Uvicorn:**

```bash
uvicorn main:app --reload
```

5. **Run backend tests with pytest:**

```bash
pytest -v tests.py
```

## Frontend

To set up and run the frontend application, follow these steps:

1. **Navigate to the frontend directory:**

```bash
cd ./frontend
```

2. **Install frontend dependencies using pnpm:**

```bash
pnpm install
```

3. **Start the frontend development server:**

```bash
pnpm dev
```

---

## Additional Notes

- Ensure you have Python, `pip`, and `pnpm` installed on your system.
- The backend uses a virtual environment located at `backend/venv`.
- The frontend uses `pnpm` for package management and development server.


## Running Tests

### Backend

To run backend tests, ensure your virtual environment is activated and run:

```bash
cd ./backend
pytest -v tests.py
```

### Frontend

To run frontend tests, use the following commands:

```bash
cd ./frontend
pnpm test
```

Refer to the frontend documentation for more details on available test scripts.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
