from browser import document, window, alert, load, bind
from browser.html import TABLE,THEAD,TBODY, TR, TH, TD, P, CANVAS, P
import math

load("https://cdn.jsdelivr.net/npm/regression@2.0.1/dist/regression.min.js")
load("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js")

dados = []

g = { 
  'type': 'scatter',
  'data': {
    'datasets': [
      {'data':[],'backgroundColor': 'black', 'label': 'Bruto'},
      {'data':[],'type':'line','fill':'false','pointRadius':0,'borderColor': 'red','label':'RL'}
    ]
  }
}
ctx = CANVAS()
ctx.attrs['id'] = 'grafico'
grafico = window.Chart.new(ctx,g)

def atualizar_grafico(d,indice):
  dados_grafico = [{'x':i[0], 'y':i[1]} for i in d] 
  grafico['data']['datasets'][indice]['data'] = dados_grafico
  grafico.update()

def obter_dados_grafico(indice):
  # dados_grafico = [{'x':i[0], 'y':i[1]} for i in d] 
  dados_grafico = grafico['data']['datasets'][indice]['data']
  dados = [[i['x'],i['y']] for i in dados_grafico]
  return dados

def criar_tabela(linhas):
  tabela = TABLE() 
  tabela <= THEAD(TR(TH('x') + TH('y')))
  corpo_tabela = TBODY()
  for linha in linhas:
    corpo_tabela <= TR(TD(linha[0]) + TD(linha[1]))
  tabela <= corpo_tabela 
  tabela.attrs['id'] = 'tabela_dados' 
  tabela.attrs['class'] = 'striped'
  return tabela  

def adicionar_coluna(coluna):
  tabela = document['tabela_dados'] 
  tabela.get(selector='THEAD')[0].get(selector='TR')[0]<= TH('RL')   
  linhas = tabela.get(selector='TBODY')[0].get(selector='TR')
  for i, linha in enumerate(linhas):
    linha <= TD(coluna[i])

def obter_dados():
  dados_brutos = []
  linhas = document["coleta_manual"].value.split('\n')
  for linha in linhas:
    linha = linha.strip()
    if linha[0] != '#':
      x,y = linha.split(' ')
      dados_brutos.append((float(x),float(y)))
  return dados_brutos 

@bind(document["coleta_manual"],"blur")
def processar(ev):
  global dados
  dados = obter_dados()
  atualizar_grafico(dados,0)
  document['grafico'] <= ctx
  document['tabela'].text = ''
  document['tabela'] <= criar_tabela(dados)
  document['tabela'].style.display = "inherit"
  document['coleta_manual'].style.display = "none"

@bind(document["tabela"],"click")
def editar_tabela(ev):
  global dados
  document['tabela'].style.display = "none" 
  document['coleta_manual'].style.display = "inherit"
   
@bind(document["ajuste_curva"],"change")
def ajuste_curva(ev):
  global dados 
  op = [opcao.index for opcao in ev.target if opcao.selected][0]
  dados_brutos = obter_dados_grafico(0)
  if op == 1:
    regressao = window.regression.linear(dados_brutos)
    atualizar_grafico(regressao.points,1)
    b, a = regressao.equation
    r2 = regressao.r2
    document['equacao_regressao'].text = f'A={a} B={b} R2= {r2}'
  elif op == 2:
    regressao = window.regression.exponential(dados_brutos)
    atualizar_grafico(regressao.points,1)
    b, a = regressao.equation
    r2 = regressao.r2
    document['equacao_regressao'].text = f'A={a} B={b} R2= {r2}'
  elif op == 3:
    regressao = window.regression.logarithmic(dados_brutos)
    atualizar_grafico(regressao.points,1)
    b, a = regressao.equation
    r2 = regressao.r2
    document['equacao_regressao'].text = f'A={a} B={b} R2= {r2}'
  else:
    dados = dados_brutos
    atualizar_grafico([],1)
    atualizar_grafico(dados,0)
    document['equacao_regressao'].text = ''

@bind(document["linealizacao"],"change")
def ajuste_curva(ev):
  global dados 
  document["ajuste_curva"].options[0].selected = True
  op = [opcao.index for opcao in ev.target if opcao.selected][0]

  if op == 2:
    linealizacao = [(i[0]**2,i[1]) for i in dados]
  elif op == 3:
    linealizacao = [(i[0]**0.5,i[1]) for i in dados]
  elif op == 4:
    linealizacao = [(math.log(i[0]),i[1]) for i in dados]  
  elif op == 5:
    linealizacao = [(math.log(i[0]),i[1]) for i in dados] 
  else:
    linealizacao = dados  

  atualizar_grafico(linealizacao,0)
  atualizar_grafico([],1)
  document['equacao_regressao'].text = ''

def coletar_dados(ev):
  window.ble_write_value()
  window.monitorarSensor()

@bind(document["conectar"],"click")
def conectar(ev):
  if ev.target.checked:
    window.conectar_ble()
  else:
    window.desconectar_ble()
