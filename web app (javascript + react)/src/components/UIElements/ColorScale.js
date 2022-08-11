import {Col, Row} from 'antd';
import React  from 'react';
import {MapState} from "../../App";
import {Colors} from "../../assets/colors";

const ColorScale = ({max, showRelative, mapState}) => {
    return (
        <div>
            <Row justify="end">
                <span>{'Instagram users talking about this'}</span>
            </Row>
            <Row justify="space-between">
                <Col>
                    0
                </Col>
                <Col>
                    {showRelative? '>' + max.relative * 100 + '%': '> ' + max.absoluteMap + ''}
                </Col>
            </Row>
            <Row>
                <div id="colorscale" style={{background: `linear-gradient(90deg, rgba(255,255,255,1) 0%, ${
                        mapState === MapState.hashtags ? Colors.hashtags : Colors.posts
                    } 100%)`}}></div>
            </Row>

        </div>
    );
}

export default ColorScale;