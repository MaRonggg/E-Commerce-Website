// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

const product_id = null;

// Allow users to send messages by pressing enter instead of clicking the Send button
document.addEventListener("keypress", function (event) {
    if (event.code === "Enter") {
        offerPrice();
    }
});

// Read the comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
function offerPrice() {
    const priceBox = document.getElementById("offered_price");
    const price = priceBox.value;
    priceBox.value = "";
    priceBox.focus();
    if (price !== "") {
        socket.send(JSON.stringify({'product_id': this.product_id, 'price': price}));
    }
}

// Called whenever data is received from the server over the WebSocket connection
socket.onmessage = function (ws_message) {
    const price = JSON.parse(ws_message.data).price;
    const highestBidDisplay = document.getElementById('highestBid');
    highestBidDisplay.innerHTML = 'Highest Bid: ' + price;
}

function auctionPage(product_id) {
    this.product_id = product_id;
    $.get('/get_one_product/' + product_id, function (product) {
        const currHighestBid = product['product_price'] != -1 ? product['product_price'] : 'Currently No Bids';
        const highestBidDisplay = document.getElementById('highestBid');
        highestBidDisplay.innerHTML = 'Highest Bid: ' + currHighestBid;

        const infoDisplay = document.getElementById('info');
        infoDisplay.innerHTML =
            '<table>' +
            '<tr>' +
            '<td><img src="/' + product['product_image'] + '" width="300" height="300"></td>' +
            '<td>Name: ' + product['product_name'] + '<br>' +
            'Description: ' + product['product_description'] + '<br>' +
            'Auction Deadline: ' + product['auction_end_time'].replace('T', ' ') + '<br>' +
            '</tr>' +
            '</table>';
    })
}