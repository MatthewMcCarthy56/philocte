import React from 'react';
import styles from './Card.module.css'

import arrow from "./assets/arrow.png"

// Props: cardInfo, color, hp, onClick
const Card = (props) => {
    const clickHandler = () => {
        if (props.onClick) {
            props.onClick(props.cardInfo);
        }
    }
    var hasArrow = [false, false, false, false, false, false, false, false];
    for (var a of props.cardInfo.arrow_ids) {
        hasArrow[a] = true;
    }
    let show = (i) => (hasArrow[i] ? 'auto' : 'none');
    return (
        <div className={styles.wrapper} style={{backgroundColor: props.color}} onClick={clickHandler}>
            <div className={styles.upperLeft}>
                <img src={arrow} className={styles.arrow} style={{transform: "rotate(-135deg)", display: show(0)}}/>
            </div>
            <div className={styles.upperMid}>
                <img src={arrow} className={styles.arrow} style={{ transform: "rotate(-90deg)", display: show(1) }} />
            </div>
            <div className={styles.upperRight}>
                <img src={arrow} className={styles.arrow} style={{ transform: "rotate(-45deg)", display: show(2) }} />
            </div>
            <div className={styles.middleRight}>
                <img src={arrow} className={styles.arrow} style={{ transform: "rotate(0deg)", display: show(3) }} />
            </div>
            <div className={styles.bottomRight}>
                <img src={arrow} className={styles.arrow} style={{ transform: "rotate(45deg)", display: show(4) }} />
            </div>
            <div className={styles.bottomMid}>
                <img src={arrow} className={styles.arrow} style={{ transform: "rotate(90deg)", display: show(5) }} />
            </div>
            <div className={styles.bottomLeft}>
                <img src={arrow} className={styles.arrow} style={{ transform: "rotate(135deg)", display: show(6) }} />
            </div>
            <div className={styles.middleLeft}>
                <img src={arrow} className={styles.arrow} style={{ transform: "rotate(180deg)", display: show(7) }} />
            </div>
            <div className={styles.middle}>
                <div className={styles.cardInfo}>
                    <div className={styles.hpValue}>
                        {props.hp}/{props.cardInfo.max_hp}
                    </div>
                    <div className={styles.attackValue}>
                        {props.cardInfo.attack_strength.toString() + props.cardInfo.attack_type}
                    </div>
                    <div className={styles.name}>
                        {props.cardInfo.name}
                    </div>
                    <div className={styles.physicalDefense}>
                        {props.cardInfo.physical_defense}
                    </div>
                    <div className={styles.magicalDefense}>
                        {props.cardInfo.magical_defense}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Card;