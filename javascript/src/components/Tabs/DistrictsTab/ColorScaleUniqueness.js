import {Col, Row} from 'antd';
import React  from 'react';
import {Colors} from "../../../assets/colors";

const ColorScaleUniqueness = () => {
    return (
        <Row justify="end">
            <div style={{width: '200px'}}>
            <Row justify="space-between">
                <Col>
                    {'not unique'}
                </Col>
                <Col>
                    {'very unique'}
                </Col>
            </Row>
            <Row justify="end">
                <div id="colorscale" style={{background: `linear-gradient(90deg, rgba(255,255,255,1) 0%, ${
                       Colors.district
                    } 100%)`}}></div>
            </Row>
            </div>
        </Row>
    );
}

export default ColorScaleUniqueness;