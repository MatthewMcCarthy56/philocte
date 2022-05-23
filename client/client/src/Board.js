import React from 'react';

import Card from './Card'
import styles from './Board.module.css'

const Board = (props) => {
    var width = props.board.length
    var height = props.board[0].length
    var table = []
    for (var i = 0; i < height; i++) {
        var row = []
        for (var j = 0; j < width; j++) {
            let cell = props.board[j][i];
            if (cell == null) {
                row.push(<td key={j}><div className={styles.empty}></div></td>)
            } else if (cell.type == 'card') {
                row.push(<td key={j}><Card /></td>)
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