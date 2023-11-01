import streamlit as st
import joblib
import pandas as pd

st.set_page_config(
    page_title="Калькулятор",
    page_icon="👋",
)

models = {}
models['mlp'] = joblib.load('models/mlp.joblib')
models['rfc'] = joblib.load('models/rfc.joblib')
models['gnb'] = joblib.load('models/gnb.joblib')
models['logreg'] = joblib.load('models/logreg.joblib')

st.write("# Анализ наличия/отсутствия ЖЭС")
data = {}
data['Возраст'] = st.slider('Возраст', min_value=10, max_value=59, value=14)
data['Рост,м'] = st.slider('Рост, м', min_value=1.2, max_value=2.0, value=1.86)
data['ЧСС ночью Макс'] = st.slider('ЧСС ночью, макс', min_value=69, max_value=149, value=98)
data['САДd'] = st.slider('САДd', min_value=88, max_value=136, value=102)
data['САДs'] = st.slider('САДs', min_value=90, max_value=134, value=100)
data['Кол-во эпизодов синусовой тахикардии'] = st.slider('Кол-во эпизодов синусовой тахикардии', min_value=0, max_value=235, value=32)
data['pNN50 день'] = st.slider('pNN50, день', min_value=0.9, max_value=33.1, value=19.0)
data['Эпизоды сердцебиений'] = st.selectbox('Эпизоды сердцебиений', ['Нет', 'Да'])
data['Индекс Варге (ИВ)'] = st.slider('Индекс Варге (ИВ)', min_value=1.08, max_value=2.5, value=1.479)
data['Итог'] = st.slider('Фены, Итог', min_value=3.99, max_value=87.83, value=61.44)

def models_report(data):
    keys = ['Рост,м', 'ЧСС ночью Макс', 'САДd', 'САДs',
       'Кол-во эпизодов синусовой тахикардии', 'pNN50 день',
       'Эпизоды сердцебиений', 'Индекс Варге (ИВ)', 'Итог', 'Возраст']
    df = pd.Series(data).to_frame().T
    df = df[keys]

    st.write('---')
    st.write('# Результат')

    st.write('### Нейронная сеть')
    st.write(f"Результат: {'Обнаружено ЖЭС' if models['mlp'].predict(df)[0] else 'ЖЭС не обнаружено'}")
    st.write(f"Достоверность наличия ЖЭС: {models['mlp'].predict_proba(df)[0][1]}")
    st.write(f"Достоверность отсутствия ЖЭС: { models['mlp'].predict_proba(df)[0][0]}")

    st.write('### Байесовский классификатор')
    st.write(f"Результат: {'Обнаружено ЖЭС' if models['gnb'].predict(df)[0] else 'ЖЭС не обнаружено'}")
    st.write(f"Достоверность наличия ЖЭС: {models['gnb'].predict_proba(df)[0][1]}")
    st.write(f"Достоверность отсутствия ЖЭС: { models['gnb'].predict_proba(df)[0][0]}")

    st.write('### Логистическая регрессия')
    st.write(f"Результат: {'Обнаружено ЖЭС' if models['logreg'].predict(df)[0] else 'ЖЭС не обнаружено'}")
    st.write(f"Достоверность наличия ЖЭС: {models['logreg'].predict_proba(df)[0][1]}")
    st.write(f"Достоверность отсутствия ЖЭС: { models['logreg'].predict_proba(df)[0][0]}")

    st.write('### Случайный лес (деревья решений)')
    st.write(f"Результат: {'Обнаружено ЖЭС' if models['rfc'].predict(df)[0] else 'ЖЭС не обнаружено'}")
    st.write(f"Достоверность наличия ЖЭС: {models['rfc'].predict_proba(df)[0][1]}")
    st.write(f"Достоверность отсутствия ЖЭС: { models['rfc'].predict_proba(df)[0][0]}")

if st.button('Получить результат'):
    data['Эпизоды сердцебиений'] = 1 if data['Эпизоды сердцебиений'] == 'Да' else 0
    models_report(data)