import './App.css';
import Map from "./components/Map/Map";
import {useEffect, useState} from "react";
import data from './assets/potatoes.json';
import {Row, Col, Layout, Tabs} from 'antd';

import MapTags from "./components/UIElements/MapTags";

import AbsoluteRelativeSwitch from "./components/UIElements/AbsoluteRelativeSwitch";
import {Content, Footer, Header } from "antd/es/layout/layout";
import Sider from "antd/es/layout/Sider";
import ClustersBox, {BubbleLayout} from "./components/Boxes/ClustersBox";
import ColorScale from "./components/UIElements/ColorScale";
import HistogramBox from "./components/Boxes/HistogramBox";
import Card from "./components/UIElements/Card"

import CountsPerQuarter from "./utils/CountsPerQuarter";
import SkylineBox from "./components/Boxes/SkylineBox";
import {Texts} from "./assets/texts";
import {Sizes} from "./assets/constants";
import HashtagSelect from "./components/UIElements/HashtagSelect";
import Posts from "./components/Boxes/Posts";

export const MapState = {
    postCount: 'post count',
    hashtags: 'hashtags',
};

function App() {

    const { TabPane } = Tabs;

    const [selectedId, setSelectedId] = useState(undefined);
    const [hoverId, setHoverId] = useState(undefined);
    const [selectedHashtags, setSelectedHashtags] = useState([]);
    const [selectedCluster, setSelectedCluster] = useState(undefined);
    const [showRelative, setShowRelative] = useState(false);
    const [max, setMax] = useState({'absolute': 0, 'relative': 0, 'absoluteMap': 0});
    const [countsPerQuarter, setCountsPerQuarter] = useState(CountsPerQuarter(selectedHashtags, selectedCluster));
    const [mapState, setMapState] = useState(MapState.postCount);

    function addHashtag(hashtag) {
        let newHashtags = [...selectedHashtags];
        if (!selectedHashtags.includes(hashtag)) {
            newHashtags.push(hashtag);
            setSelectedHashtags(newHashtags);
        }
    }

    function removeHashtag(hashtag) {
        let newHashtags = [...selectedHashtags];
        newHashtags = newHashtags.filter(v => v !== hashtag);
        setSelectedHashtags(newHashtags);
    }

    useEffect(() => {
            if (selectedHashtags.length === 0 && !selectedCluster) {
                setMapState(MapState.postCount);
            } else {
                setMapState(MapState.hashtags);
            }
        }, [selectedHashtags, selectedCluster]
    )

    useEffect(() => {
        setCountsPerQuarter(CountsPerQuarter(selectedHashtags, selectedCluster));
    }, [selectedHashtags, selectedCluster]);


    useEffect(() => {
        let valuesAbsolute = Object.keys(countsPerQuarter).map(id => countsPerQuarter[id].count);
        const valuesRelative = Object.keys(countsPerQuarter).map(id => countsPerQuarter[id].relativeAmount);
        const maxAbsolute = Math.max(...valuesAbsolute);
        const maxRelative = Math.max(...valuesRelative);
        const maxRelativeRounded = Math.ceil(maxRelative*100)/100;

        valuesAbsolute = valuesAbsolute.filter((v) => v!==maxAbsolute);
        const secondMaxAbsolute = Math.max(...valuesAbsolute);
        const maxAbsoluteRounded = Math.ceil(maxAbsolute/100)*100;
        const maxAbsoluteRoundedMap =  Math.ceil((secondMaxAbsolute+(maxAbsolute-secondMaxAbsolute)/5)/100)*100


        setMax(
            {
                'absolute': maxAbsoluteRounded,
                'relative': maxRelativeRounded,
                'absoluteMap': maxAbsoluteRoundedMap,
            }
        );
        },[countsPerQuarter]);

    return (
        <>
            <div id="map">
                <Map setSelectedId={setSelectedId}
                     selectedId={selectedId}
                     potatoes={data.features}
                     countsPerQuarter={countsPerQuarter}
                     showRelative={showRelative}
                     max={max}
                     mapState={mapState}
                />
            </div>

            <div className="boxes-layout App">
                <Layout>
                    <Layout>
                        <Layout>
                            <Layout>
                            <Header>
                                <div id="title">
                                    <span>{Texts.title}</span>
                                </div>
                                <Row justify="space-between">
                                    <Col span={24}>
                                        <div style={{height: '15px'}}/>
                                        <MapTags selectedHashtags={selectedHashtags} selectedId={selectedId} selectedCluster={selectedCluster} removeHashtag={removeHashtag} setSelectedId={setSelectedId} setSelectedCluster={setSelectedCluster}/>
                                    </Col>
                                </Row>
                            </Header>
                            <Content></Content>
                            <Footer>
                                <Row gutter={[16,16]} justify="space-between" align="bottom">
                                <Col>
                                    <AbsoluteRelativeSwitch showRelative={showRelative} setShowRelative={setShowRelative} mapState={mapState}/>
                                </Col>
                                <Col>
                                    <ColorScale max={max} showRelative={showRelative} mapState={mapState}/>
                                </Col>
                                    <Col span={24}>
                                        <div>
                                            <Posts selectedId={selectedId} selectedHashtags={selectedHashtags} selectedCluster={selectedCluster}/>
                                        </div>
                                </Col>
                                </Row>
                            </Footer>
                            </Layout>
                            <Sider  width={Sizes.siderWidth} >

                                <Card>
                                    <Tabs defaultActiveKey="1" id="mytabs">

                                        <TabPane tab="About" key={1}>
                                            <span>
                                                {Texts.about}
                                            </span>
                                            <HistogramBox countsPerQuarter={countsPerQuarter} max={max} setSelectedId={setSelectedId}></HistogramBox>
                                        </TabPane>

                                        <TabPane tab="Explore hashtags" key={2}>
                                            <HashtagSelect addHashtag={addHashtag}/>
                                            {selectedHashtags.length > 0 ? (
                                            <SkylineBox countsPerQuarter={countsPerQuarter} max={max} selectedId={selectedId} setSelectedId={setSelectedId} hoverId={hoverId} setHoverId={setHoverId} ></SkylineBox>
                                            ) :
                                                (
                                                    <div>
                                                        <br/>
                                                        <div><b>{Texts.selectAHashtag}</b></div>
                                                    </div>
                                                )

                                            }
                                        </TabPane>
                                        <TabPane tab="Explore districts" key={3}>
                                                    <ClustersBox selectedId={selectedId} setSelectedId={setSelectedId}
                                                                 selectedHashtags={selectedHashtags}
                                                                 addHashtag={addHashtag}
                                                                 removeHashtag={removeHashtag}
                                                                 selectedCluster={selectedCluster}
                                                                 setSelectedCluster={setSelectedCluster}/>

                                        </TabPane>
                                    </Tabs>
                                </Card>
                            </Sider>
                        </Layout>
                    </Layout>
                </Layout>
            </div>
        </>
  );
}

export default App;
