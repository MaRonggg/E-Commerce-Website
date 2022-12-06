// Establish a WebSocket connection with the server
// const socket = new WebSocket('ws://' + window.location.host + '/websocket');

// import socket from 'templates/auction_page.html'
// <script src="/socket.io/socket.io.js"></script>

const socket = io("http://" + location.host, { transports: ["websocket"] });
// const socket = io("http://localhost:8080/auction_page/product_id=${pid}", { transports: ["websocket"] });

// var socket = io({transports: ['websocket']}).connect('http://127.0.0.1:/websocket');

const product_id = null;

$(document).ready(function() {

        // const socket = io("http://localhost:8000", { transports: ["websocket"] });
        //
            socket.on('connect', function() {
                // in here, we would like to know which user connect to our auction

         	socket.send('User has connected!');
        });

        socket.on('message', function(data) {

            if (data === ''){
                alterMessage()
            }
            else {
                const highestBidDisplay = document.getElementById('highestBid');
                highestBidDisplay.innerHTML = 'Highest Bid: $' + data.price.toFixed(2);
                const msg = data.username + ' offered $' + data.price.toFixed(2) + ' for ' + data.productName + '!'
                $("#price").append('<li>'+msg+'</li>');
            }

            console.log('Received message');
        });

        // // $('#sendbutton').on('click', function() {
        //     socket.send($('#offered_price').val());
        //     $('#offered_price').val('');
        // });

    });

function alterMessage(){
    alert('Invalid bid. Enter price is lower than the current highest price. ')
}

// Allow users to send messages by pressing enter instead of clicking the Send button
document.addEventListener("keypress", function (event) {
    if (event.code === "Enter") {
        offerPrice();
    }
});

// Read the comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
function offerPrice() {
    if (checkPrice()) {
        const priceBox = document.getElementById("offeredPrice");
        const price = priceBox.value;
        priceBox.value = "";
        priceBox.focus();
        if (price !== "") {
            // in here, we can to show who offer the price, we need to know the user
            // socket.send(JSON.stringify({'product_id': this.u, 'price': price}));
            socket.send(JSON.stringify({'product_id': this.product_id, 'price': price}));
        }
        // socket.send($('#myMessage').val());
        // $('#myMessage').val('');
    }
}

// Called whenever data is received from the server over the WebSocket connection
// socket.onmessage = function (ws_message) {
//     const price = JSON.parse(ws_message.data).price;
//     const highestBidDisplay = document.getElementById('highestBid');
//     highestBidDisplay.innerHTML = 'Highest Bid: ' + price;
// }

function checkPrice() {
    const price = $('#offeredPrice').val().trim();
    const flag = price.match(/^\d+(\.\d{1,2})?$/);
    if (flag) {
        document.getElementById('offeredPriceError').style.display = 'none';
    } else {
        document.getElementById('offeredPriceError').style.display = '';
    }
    return flag;
}

function auctionPage(product_id) {
    this.product_id = product_id;
    $.get('/get_one_product/' + product_id, function (product) {
        const currHighestBid = product['product_price'] != -1 ? parseFloat(product['product_price']).toFixed(2) : 'Currently No Bids';
        const highestBidDisplay = document.getElementById('highestBid');
        highestBidDisplay.innerHTML = 'Highest Bid: $' + currHighestBid;

        const infoDisplay = document.getElementById('info');
        infoDisplay.innerHTML =
            '<table>' +
            '<tr>' +
            '<td><img src="/' + product['product_image'] + '" width="300" height="300"></td>' +
            '<td>Name: ' + product['product_name'] + '<br>' +
            'Description: ' + product['product_description'] + '<br>' +
            'Auction Deadline: ' + product['auction_end_time'].replace('T', ' ') + '</td>' +
            '</tr>' +
            '</table>';
    })
}