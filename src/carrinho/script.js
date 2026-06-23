$(document).ready(function() {
    const carrinho = JSON.parse(localStorage.getItem("carrinho")) || []
    const listElement = $('#lista')
    const totalElement = $("#total")

    function exibirCarrinho(){
        listElement.empty()
        let totalPreco = 0

        $.each(carrinho, function(index, item){
            const listItem = $("<li>").text(`${item.desc} - Preço: $${item.sal}`)

            const removeButton = $("<button>").text("❌").css("margin-left", "10px").click(function()
            {
                removerItem(index)
            })

            listItem.append(removeButton)
            listElement.append(listItem)

            totalPreco += parseFloat(item.sal)
        })
        totalElement.text(`Total $${totalPreco}`)
    }

    function removerItem(index){
        carrinho.splice(index, 1)
        localStorage.setItem("carrinho", JSON.stringify(carrinho))
        exibirCarrinho()
    }
    exibirCarrinho()
})
function gerar(){
    const listElement = document.getElementById("lista")
    const totalElement = document.getElementById("total")
    const listaClone = listElement.cloneNode(true)
    $(listaClone).find("button").remove()
    const listaHtml = listaClone.innerHTML
    const totalHtml = totalElement.innerHTML
    const conteudoHTML = `
        <html>
            <head>
                <meta charset="UTF=8">
            </head>
            <body>
                <h1>PEDIDO CONFIRMADO</h1>
                <h3>Agradeceos sua compra e sua preferência.</h3>
                <br>
                ${listaHtml}
                <br>
                <br>
                ${totalHtml}
            </body>
        </html>
    `
    const blob = new Blob([conteudoHTML], {type: "application/msword"})
    const link = document.createElement("a")

    link.href = URL.createObjectURL(blob)
    link.download = "pedido.doc"
    link.click()
    document.getElementById("pedido").style.display = "block"
}

function successClose(){
    document.getElementById("pedido").style.display = "none"
}