name: Run Spoonacular Script

on:
  workflow_dispatch:   # allows manual run
  push:
    branches: ["main"] # OR choose your branch

jobs:
  run-script:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install requests

      - name: Run script
        env:
          SPOONACULAR_KEY: ${{ secrets.SPOONACULAR_KEY }}
        run: python run_spoonacular.py
