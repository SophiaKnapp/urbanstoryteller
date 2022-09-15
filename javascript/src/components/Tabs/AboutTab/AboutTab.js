import React from 'react';
import '../../../App.css';
import {Texts} from "../../../assets/texts";
import UserCountChart from "./UserCountChart";

const AboutTab = ({selectedId, setSelectedId, countsPerQuarter, max}) => {
    return (
            <div className='sider-card'>
                                            <span>
                                                {Texts.about}
                                            </span>
                    <UserCountChart countsPerQuarter={countsPerQuarter} max={max} selectedId={selectedId} setSelectedId={setSelectedId}></UserCountChart>
            </div>
    )
}
export default AboutTab;