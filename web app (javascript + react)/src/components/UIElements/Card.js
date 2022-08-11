import React from 'react'
import '../../App.css';

import { Typography } from "antd";


function Card({ title, description, children }) {
    return (
        <>
        <div className="card">
            {/*<div>*/}
            {/*    <div className="title">*/}
            {/*        {title}*/}
            {/*    </div>*/}
            {/*    <div className="description">*/}
            {/*        {description}*/}
            {/*    </div>*/}
            {/*</div>*/}
            {children}
        </div>
        </>
    )
}

// function Box({ children, ...props }) {
//     return <div {...props}>{children}</div>
// }

export default Card;