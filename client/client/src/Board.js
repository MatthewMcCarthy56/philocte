import React from 'react';

import Card from './Card'
import styles from './Board.module.css'

// Props: board, spaceOnClick, cardOnClick
const Board = (props) => {
    var width = props.board.length
    var height = props.board[0].length
    var table = []
    for (let i = 0; i < height; i++) {
        var row = []
        for (let j = 0; j < width; j++) {
            let cell = props.board[j][i];
            if (cell == null) {
                const spaceClick = () => {
                    if (props.spaceOnClick) props.spaceOnClick(j, i);
                }
                row.push(<td key={j}><div className={styles.empty} onClick={spaceClick}></div></td>)
            } else if (cell.type == 'card') {
                const color = cell.controller == 0 ? 'blue' : 'orange';
                const cardClick = (card) => {
                    if (props.cardOnClick) props.cardOnClick(j, i, card);
                }
                row.push(<td key={j}><Card cardInfo={cell.card} color={color} hp={cell.hp} onClick={cardClick} /></td>)
            } else {
                row.push(<td key={j}><div className={styles.wall}></div></td>)
            }
        }
        table.push(<tr key={i}>{row}</tr>)
    }
    return (
        <div>
            <table>
                <tbody>
                    {table}
                </tbody>
            </table>
        </div>
    )
}

export default Board;