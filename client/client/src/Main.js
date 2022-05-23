import './Main.css';
import Card from './Card'
import Hand from './Hand'
import Board from './Board'
import Deck from './Deck'
import React, { useEffect, useState } from 'react';

const ws = new WebSocket('ws://localhost:5000');
const maxHand = 8;
const arrowDirections = [
    [-1, -1],
    [0, -1],
    [1, -1],
    [1, 0],
    [1, 1],
    [0, 1],
    [-1, 1],
    [-1, 0]
]
const arrowOpposites = [4, 5, 6, 7, 0, 1, 2, 3];

function Main(props) {
    var [playerId, setPlayerId] = useState(null);
    var [board, setBoard] = useState(null);
    var [deck, setDeck] = useState(null);
    var [hand, setHand] = useState(null);
    var [opponentHand, setOpponentHand] = useState(null);
    var [currentPlayer, setCurrentPlayer] = useState(null);
    var [selectedCard, setSelectedCard] = useState(null);
    var [selectedSpace, setSelectedSpace] = useState(null);
    var [neededBattles, setNeededBattles] = useState(null);
    var [selectedBattles, setSelectedBattles] = useState(null);
    useEffect(() => {
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
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
        const cardClick = (card) => {
            if (currentPlayer != playerId) return;
            setSelectedCard(card);
            setSelectedSpace(null);
            setNeededBattles(null);
            setSelectedBattles(null);
        };
        var spaceClick = null;
        if (selectedCard) {
            spaceClick = (x, y) => {
                console.log("Play at", x, y);
                const battles = new Map();
                var battleDirections = [];
                for (let arrow of selectedCard.arrow_ids) {
                    console.log(arrow, typeof(arrow));
                    const targetX = x + arrowDirections[arrow][0];
                    const targetY = y + arrowDirections[arrow][1];
                    console.log(targetX, targetY);
                    if (targetX < 0 || targetX >= board.length || targetY < 0 || targetY >= board[0].length) continue;
                    const targeted = board[targetX][targetY];
                    console.log(targeted);
                    if (!targeted || targeted.type != "card") continue;
                    if (targeted.controller == playerId) continue;
                    const targetArrows = targeted.card.arrow_ids;
                    console.log(targetArrows);
                    if (targetArrows.includes(arrowOpposites[arrow])) {
                        battles.set(targeted.card.id, arrow);
                        battleDirections.push(arrow);
                    }
                }
                if (battles.size < 2) {
                    console.log(battleDirections);
                    ws.send(JSON.stringify({
                        card: selectedCard.id,
                        position: [x, y],
                        battle_order: battleDirections
                    }));
                    setSelectedCard(null);
                } else {
                    setSelectedSpace([x, y]);
                    setNeededBattles(battles);
                    setSelectedBattles([]);
                }
            };
        }
        var battleClick = null;
        if (selectedSpace && neededBattles) {
            battleClick = (x, y, card) => {
                if (!neededBattles.has(card.id) || selectedBattles.includes(card.id)) return;
                selectedBattles.push(neededBattles.get(card.id));
                if (selectedBattles.length == neededBattles.size) {
                    ws.send(JSON.stringify({
                        card: selectedCard.id,
                        position: selectedSpace,
                        battle_order: selectedBattles
                    }));
                    setSelectedCard(null);
                    setSelectedSpace(null);
                    setNeededBattles(null);
                    setSelectedSpace(null);
                }
            };
        }
        return (
            <div>
                <Hand cardInfo={opponentHand} color={opponentColor}></Hand>
                <Board board={board} spaceOnClick={spaceClick} cardOnClick={battleClick}></Board>
                <Hand cardInfo={hand} color={userColor} cardOnClick={cardClick}></Hand>
            </div>
        );
    }
}

export default Main;
