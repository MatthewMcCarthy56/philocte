import React from 'react'

import styles from './Hand.module.css'
import Card from './Card'

// Props: cardInfo, color
const Hand = (props) => {

    return (
        <div className={styles.playerHand}>
            {props.cardInfo.map((element, index) => (
                <Card key={index} cardInfo={element} color={props.color} hp={element.max_hp} />
            ))}
        </div>
    )
}

export default Hand;