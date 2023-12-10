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

st.write("# Анализ вероятности развития ЖЭС")
data = {}
data['Возраст'] = st.slider('Возраст, лет', min_value=10, max_value=59, value=14)
data['Рост,м'] = st.slider('Рост, м', min_value=1.2, max_value=2.0, value=1.86)
data['Вес'] = st.slider('Вес, кг', min_value=26.0, max_value=85.0, value=56.0)

data['Эпизоды сердцебиений'] = st.selectbox('Эпизоды сердцебиений', ['Нет', 'Да'])
data['Головокружение'] = st.selectbox('Головокружение', ['Нет', 'Да'])

data['САДd'] = st.slider('САДd', min_value=88.0, max_value=136.0, value=102.0)
data['САДs'] = st.slider('САДs', min_value=90.0, max_value=134.0, value=100.0)

data['Итог'] = st.slider('Суммарный диагностический коэффициент НДСТ', min_value=3.99, max_value=87.83, value=61.44)


def models_report(data):
    keys = ['Вес', 'Головокружение', 'Рост,м', 'САДd', 'ИМТ', 'САДs',
       'Эпизоды сердцебиений', 'Индекс Варге (ИВ)', 'Итог', 'Возраст']
    df = pd.Series(data).to_frame().T
    df = df[keys]
    st.write('---')

    st.write(f"ИМТ: {data['ИМТ']}")
    st.write(f"Индекс Варге (ИВ): {data['Индекс Варге (ИВ)']}")


    st.write('---')
    st.write('# Результат')

    st.write('### Нейронная сеть')
    st.write(f"Результат: {'Вероятно развитие ЖЭС' if models['mlp'].predict(df)[0] else 'ЖЭС не обнаружено'}")
    st.write(f"Достоверность развития ЖЭС: {models['mlp'].predict_proba(df)[0][1]}")
    st.write(f"Достоверность отсутствия ЖЭС: { models['mlp'].predict_proba(df)[0][0]}")

    st.write('### Байесовский классификатор')
    st.write(f"Результат: {'Вероятно развитие ЖЭС' if models['gnb'].predict(df)[0] else 'ЖЭС не обнаружено'}")
    st.write(f"Достоверность развития ЖЭС: {models['gnb'].predict_proba(df)[0][1]}")
    st.write(f"Достоверность отсутствия ЖЭС: { models['gnb'].predict_proba(df)[0][0]}")

    st.write('### Логистическая регрессия')
    st.write(f"Результат: {'Вероятно развитие ЖЭС' if models['logreg'].predict(df)[0] else 'ЖЭС не обнаружено'}")
    st.write(f"Достоверность развития ЖЭС: {models['logreg'].predict_proba(df)[0][1]}")
    st.write(f"Достоверность отсутствия ЖЭС: { models['logreg'].predict_proba(df)[0][0]}")

    st.write('### Случайный лес (деревья решений)')
    st.write(f"Результат: {'Вероятно развитие ЖЭС' if models['rfc'].predict(df)[0] else 'ЖЭС не обнаружено'}")
    st.write(f"Достоверность развития ЖЭС: {models['rfc'].predict_proba(df)[0][1]}")
    st.write(f"Достоверность отсутствия ЖЭС: { models['rfc'].predict_proba(df)[0][0]}")

if st.button('Получить результат'):
    data['Эпизоды сердцебиений'] = 1 if data['Эпизоды сердцебиений'] == 'Да' else 0
    data['Головокружение'] = 1 if data['Головокружение'] == 'Да' else 0

    data['ИМТ'] = data['Вес'] / (data['Рост,м']*data['Рост,м'])
    data['Индекс Варге (ИВ)'] = (data['Вес']*1000) / ((data['Рост,м']*100)**2) - (data['Возраст']/100)
    
    models_report(data)