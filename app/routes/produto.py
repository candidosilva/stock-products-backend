from bson.objectid import ObjectId
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..extentions.database import mongo

produto = Blueprint("produto", __name__)

@produto.route('/list')
def listProdutos():
    if "username" in session:
        produtos = mongo.db.produtos.find()
        return render_template("produtos/list.html", produtos=produtos)
    else:
        redirect(url_for('usuario.index'))
    
@produto.route('/insert', methods=["GET", "POST"])
def insertProdutos():
    if request.method == 'GET':
        return render_template("produtos/insert.html")
    else:
        nome = request.form.get('nome')
        quantidade = request.form.get('quantidade')
        preco = request.form.get('preco')
        categoria = request.form.get('categoria')
        estoque = request.form.get('estoque')
        if not nome or len(nome) > 50:
            flash("Campo 'nome', é obrigatório e deve ser menor que 50 caracteres")
        elif not quantidade or not quantidade.isdigit() or int(quantidade) <= 0:
            flash("Campo quantidade é obrigatório")
        elif not preco:
            flash('Campo preço é obrigatório')
        elif not categoria:
            flash('Campo categoria é obrigatório')
        elif not estoque:
            flash('Campo estoque é obrigatório')
        else:
            mongo.db.produtos.insert_one({
                "produto": nome,
                "quantidade": quantidade,
                "preco": preco,
                "categoria": categoria,
                "estoque": estoque,
                "valor_total": (float(quantidade) * float(preco))
            })
        return redirect(url_for("produto.listProdutos"))

    
@produto.route('/edit', methods=["GET", "POST"])
def editProdutos():
    if request.method == "GET":
        idproduto = request.values.get('idproduto')

        if not idproduto:
            flash("Campo idproduto é obrigatório")
            return redirect(url_for("produto.listProduto"))
        else:
            idprod = mongo.db.produtos.find({"_id": ObjectId(idproduto)})
            produto = [prd for prd in idprod]
            print(produto)
            estoques = set()
            produtos = mongo.db.produtos.find()
            for p in produtos:
                estoques.add(p['estoque'])
            return render_template("produtos/edit.html", produto=produto, estoques=estoques)

    else:
        idproduto = request.form.get('idproduto')
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        estoque = request.form.get('estoque')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')

        mongo.db.produtos.update_one({"_id": ObjectId(idproduto)},{
            "$set": {
                "produto": nome,
                "quantidade": quantidade,
                "preco": preco,
                "categoria": categoria,
                "estoque": estoque,
                "valor_total": (float(quantidade) * float(preco))
            }
        })
        flash("Produto alterado com sucesso")
    return redirect(url_for("produto.listProdutos"))
    
@produto.route('/delete')
def deleteProdutos():
    idproduto = request.values.get('idproduto')

    mongo.db.produtos.delete_one({"_id": ObjectId(idproduto)})
    flash("produto deletado com sucesso")

    return redirect(url_for("produto.listProdutos"))