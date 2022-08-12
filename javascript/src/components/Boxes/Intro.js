import React from 'react';
import '../../App.css';
import Card from '../UIElements/Card';
import {Col} from "antd";

const Intro = () => {

    return (
        <Card title={"Info Box"} description={""}>
            <Col span={23}>
                <div id="intro">
                    <div id="intro-title">
                        <span>
                        Instagram image of munich
                            </span>
                    </div>
                    <div id="intro-text">
                        <span>
                        Welcome to instagram image of munich.
                        This is a description.
                        Search for hashtags you're interested in or select a district to get started.
                            </span>

                    </div>
                </div>
            </Col>
    </Card>
    );
}
export default Intro;