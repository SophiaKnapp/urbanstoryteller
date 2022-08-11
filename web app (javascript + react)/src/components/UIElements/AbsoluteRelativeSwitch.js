import { Radio } from 'antd';
import React from 'react';

const AbsoluteRelativeSwitch = ({showRelative, setShowRelative}) => {
    return (
        <Radio.Group value={showRelative ? "relative" : "absolute"} onChange={e => {
                if (e.target.value == "absolute") {
                    setShowRelative(false);
                } else {
                    setShowRelative(true);
                }
            }
        }>
            <Radio.Button value="absolute">Absolute</Radio.Button>
            <Radio.Button value="relative">Relative</Radio.Button>
        </Radio.Group>
    );
}

export default AbsoluteRelativeSwitch;