$(document).ready(function() {
    const carrinho = JSON.parse(localStorage.getItem("carrinho")) || []
    const listElement = $('#lista')
    const totalElement = $("#total")

    function exibirCarrinho(){
        listElement.empty()
        let totalPreco = 0

        $.each(carrinho, function(index, item){
            const listItem = $("<li>").text(`${item.desc} - Preço: $${item.preco.toFixed(2)}`)

            const removeButton = $("<button>").text("❌").css("margin-left", "10px").click(function(){
                removerItem(index)
            })

        })
    }

})