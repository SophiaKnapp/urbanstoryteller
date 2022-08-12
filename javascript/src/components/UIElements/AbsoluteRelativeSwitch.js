import { Radio } from 'antd';
import React from 'react';
import {MapState} from "../../App";

const AbsoluteRelativeSwitch = ({showRelative, setShowRelative, mapState}) => {
    return (
        <Radio.Group value={showRelative ? "relative" : "absolute"} onChange={e => {
                if (e.target.value == "absolute") {
                    setShowRelative(false);
                } else {
                    setShowRelative(true);
                }
            }
        } disabled={mapState===MapState.postCount}>
            <Radio.Button value="absolute">Absolute</Radio.Button>
            <Radio.Button value="relative">Relative</Radio.Button>
        </Radio.Group>
    );
}

export default AbsoluteRelativeSwitch;