import './Main.css';
import Card from './Card'
import Hand from './Hand'
import Board from './Board'
import Deck from './Deck'
import React, { useEffect, useState } from 'react';

const ws = new WebSocket('ws://localhost:5000');
const maxHand = 8;

function Main(props) {
    var [playerId, setPlayerId] = useState(null);
    var [board, setBoard] = useState(null);
    var [deck, setDeck] = useState(null);
    var [hand, setHand] = useState(null);
    var [opponentHand, setOpponentHand] = useState(null);
    var [currentPlayer, setCurrentPlayer] = useState(null);
    console.log(playerId);
    console.log(opponentHand);
    useEffect(() => {
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            console.log("Player ID: ");
            console.log(playerId);
            if (playerId == null) {
                // First message
                setPlayerId(message.player_id);
                setBoard(message.walls);
                setDeck(message.deck);
                setHand([]);
                console.log("Connected");
            } else if (message.winner !== undefined) {
                // Somebody won - TODO
            } else {
                // Gameplay update
                setBoard(message.board);
                setCurrentPlayer(message.current_player);
                setHand(message.player_hands[playerId]);
                setOpponentHand(message.player_hands[1 - playerId]);
                console.log("Gameplay");
            }
        };
    }, [playerId]);
    const userColor = playerId === 0 ? 'blue' : 'orange';
    const opponentColor = playerId === 0 ? 'orange' : 'blue';
    if (playerId == null) {
        return (<div>Connecting...</div>);
    } else if (opponentHand == null) {
        // Hand-building phase
        const cardClick = (card) => {
            if (hand.length >= maxHand) return;
            const newDeck = deck.filter(item => item !== card);
            hand.push(card);
            setDeck(newDeck);
            setHand(hand);
            if (hand.length >= maxHand) {
                const handIds = hand.map((item, index) => item.id);
                ws.send(JSON.stringify(handIds));
            }
        };
        const status = hand.length < maxHand ? ("Select " + maxHand + " cards from your deck") : "Waiting for opponent to select hand";
        return (
            <div>
                <Deck deckInfo={deck} cardOnClick={cardClick}></Deck>
                <Board board={board}></Board>
                <Hand cardInfo={hand} color={userColor}></Hand>
                <div>{status}</div>
            </div>
        );
    } else {
        // Playing phase
        return (
            <div>
                <Hand cardInfo={opponentHand} color={opponentColor}></Hand>
                <Board board={board}></Board>
                <Hand cardInfo={hand} color={userColor}></Hand>
            </div>
        );
    }
}

export default Main;
