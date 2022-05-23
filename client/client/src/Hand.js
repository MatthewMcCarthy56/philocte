import React from 'react'

import styles from './Hand.module.css'
import Card from './Card'

// Props: cardInfo, color, cardOnClick
const Hand = (props) => {
    return (
        <div className={styles.playerHand}>
            {props.cardInfo.map((element, index) => (
                <Card key={element.id} cardInfo={element} color={props.color} hp={element.max_hp} onClick={props.cardOnClick} />
            ))}
        </div>
    )
}

export default Hand;