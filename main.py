from flask import Flask, request
import uuid

app = Flask(__name__)

historico_calculos = []

@app.route("/soma", methods=["POST"])
def somar():
    dados_recebidos = request.get_json()
    numero1 = dados_recebidos['numero1']
    numero2 = dados_recebidos['numero2']
    resultado = numero1 + numero2

    novo_calculo = {
        "id": str(uuid.uuid4()),
        "numero1": numero1,
        "numero2": numero2,
        "resultado": resultado
    }
    
    historico_calculos.append(novo_calculo)
    return novo_calculo

@app.route("/calculos", methods=["GET"])
def listar_calculos():
    return {"historico": historico_calculos}

@app.route("/deletar/<id>", methods=["DELETE"])
def deletar(id):
    global historico_calculos
    historico_calculos = [calculo for calculo in historico_calculos if calculo['id'] != id]
    
    return {"mensagem": "Cálculo removido com sucesso"}

@app.route("/editar/<id>", methods=["PUT"])
def editar(id):
    dados_recebidos = request.get_json()
    for calculo in historico_calculos:
        if calculo["id"] == id:
            calculo["numero1"] = dados_recebidos.get("numero1", calculo["numero1"])
            calculo["numero2"] = dados_recebidos.get("numero2", calculo["numero2"])
            calculo["resultado"] = calculo["numero1"] + calculo["numero2"]
            return calculo

    return {"erro": "Cálculo não encontrado"}, 404

if __name__ == "__main__":
    app.run(debug=True)
