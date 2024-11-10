# Streamlit PDF Annotator

Streamlit component that allows you to annotate PDFs easily, built with Vue3 and Vite.

## Quickstart

Ensure you have [Python 3.6+](https://www.python.org/downloads/), [Node.js](https://nodejs.org) and [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) installed.

1. Clone this repository:
``` bash
git clone git@github.com:gabrieltempass/streamlit-component-vue-vite-template.git
```

2. Go to the `frontend` directory and initialize and run the component template frontend:
``` bash
cd streamlit-component-vue-vite-template/annotator/frontend
```
``` bash
npm install
npm run dev
```

3. From a separate terminal, go to the repository root directory, create a new Python virtual environment, activate it and install Streamlit and the template as an editable package:
``` bash
cd streamlit-component-vue-vite-template
```
``` bash
python3 -m venv venv
. venv/bin/activate
pip install streamlit
pip install -e .
```

Still from the same separate terminal, run the example Streamlit app:
``` bash
streamlit run annotator/example.py
```

If all goes well, you should see something like this:

![Quickstart Success](quickstart.png)

Modify the frontend code at `annotator/frontend/src/MyComponent.vue`.
Modify the Python code at `annotator/__init__.py`.
