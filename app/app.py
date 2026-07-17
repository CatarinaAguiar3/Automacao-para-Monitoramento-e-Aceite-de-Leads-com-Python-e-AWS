from flask import Flask, render_template, request, redirect, url_for
import time


app = Flask(__name__)


# Simulação de dados
leads = [
    {
        "id": 1,
        "nome": "Rita"
    },
    {
        "id": 2,
        "nome": "Francisco"
    }
]


@app.route("/")
def login():

    return render_template(
        "login.html"
    )


@app.route("/login", methods=["POST"])
def realizar_login():

    usuario = request.form["usuario"]

    return render_template(
        "redirect.html",
        email=usuario
    )



@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        leads=leads
    )



# @app.route("/atualizar")
# Também funciona
# def atualizar():

#     # Simula atualização da lista
#     global leads

#     leads.append(
#         {
#             "id": 3,
#             "nome": "NOVO CLIENTE"
#         }
#     )


#     return redirect(
#         url_for("dashboard")
#     )
# --------------------------------------

# #################
# DEU CERTO!      #
###################
# cliente_adicionado = False
# @app.route("/atualizar")
# def atualizar():

#     global leads, cliente_adicionado

#     if not cliente_adicionado:
#         leads.append(
#             {
#                 "id": 3,
#                 "nome": "Alice"
#             }
#         )

#         cliente_adicionado = True

#     return redirect(
#         url_for("dashboard")
#     )

cliente_atualizacao = 0


@app.route("/atualizar")
def atualizar():

    global leads, cliente_atualizacao

    if cliente_atualizacao == 0:
        leads.append(
            {
                "id": 3,
                "nome": "Alice"
            }
        )

    elif cliente_atualizacao == 1:
        leads.append(
            {
                "id": 4,
                "nome": "Zangado"
            }
        )

    cliente_atualizacao += 1

    return redirect(
        url_for("dashboard")
    )



# --------------------------------------------------
# @app.route("/atualizar")
# def atualizar():

#     # Simula atualização da lista
#     global leads

#     leads.append(
#         {
#             "id": 3,
#             "nome": "NOVO CLIENTE"
#         }
#     )


#     return render_template(
#         "dashboard.html",
#         leads=leads,
#         atualizando=True
#     )


@app.route("/assumir", methods=["POST"])
def assumir():

    global leads


    if len(leads) > 0:

        cliente_assumido = leads.pop(0)


        return render_template(
            "sucesso.html",
            cliente=cliente_assumido
        )


    return redirect(
        url_for("dashboard")
    )

@app.route("/fechar_modal")
def fechar_modal():

    return redirect(
        url_for("dashboard")
    )

if __name__ == "__main__":

    app.run(
        debug=True
    )