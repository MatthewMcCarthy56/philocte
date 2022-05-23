import React from 'react'

import styles from './Deck.module.css'
import Card from './Card'

// Props: deckInfo, cardOnClick
const Deck = (props) => {
    return (
        <div className={styles.deck}>
            {props.deckInfo.map((element, index) => (
                <Card key={index} cardInfo={element} color="lightgray" hp={element.max_hp} onClick={props.cardOnClick} />
            ))}  
        </div>
    )
}

export default Deck;