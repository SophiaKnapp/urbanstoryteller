import './App.css';
import Map from "./components/Map/Map";
import {useEffect, useState} from "react";
import data from './assets/potatoes.json';
import {Row, Col, Layout, Tabs} from 'antd';
import MapTags from "./components/Map/MapTags";
import AbsoluteRelativeSwitch from "./components/Map/AbsoluteRelativeSwitch";
import {Content, Footer, Header } from "antd/es/layout/layout";
import Sider from "antd/es/layout/Sider";
import DistrictsTab from "./components/Tabs/DistrictsTab/DistrictsTab";
import ColorScaleMap from "./components/Map/ColorScaleMap";
import Card from "./utils/Card"
import CountsPerQuarter from "./utils/CountsPerQuarter";
import {Texts} from "./assets/texts";
import {Sizes} from "./assets/constants";
import PostsView from "./components/PostsView/PostsView";
import HashtagsTab from "./components/Tabs/HashtagsTab/HashtagsTab";
import AboutTab from "./components/Tabs/AboutTab/AboutTab";

export const MapState = {
    postCount: 'post count',
    hashtags: 'hashtags',
};

function App() {

    const { TabPane } = Tabs;

    const [selectedId, setSelectedId] = useState(undefined);
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
                                <Row>
                                    <Col offset={1}>
                                        <div id="title">
                                            <span>{Texts.title}</span>
                                        </div>
                                    </Col>
                                </Row>
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
                                    <ColorScaleMap max={max} showRelative={showRelative} mapState={mapState}/>
                                </Col>
                                    <Col span={24}>
                                        <div>
                                            <PostsView selectedId={selectedId} selectedHashtags={selectedHashtags} selectedCluster={selectedCluster}/>
                                        </div>
                                </Col>
                                </Row>
                            </Footer>
                            </Layout>
                            <Sider  width={Sizes.siderWidth} >
                                <Card>
                                    <Tabs defaultActiveKey="1" id="tabs">
                                        <TabPane tab="About" key={1}>
                                            <AboutTab countsPerQuarter={countsPerQuarter} max={max} selectedId={selectedId} setSelectedId={setSelectedId}/>
                                        </TabPane>
                                        <TabPane tab="Explore hashtags" key={2}>
                                            <HashtagsTab countsPerQuarter={countsPerQuarter}
                                                         max={max}
                                                         selectedId={selectedId}
                                                         setSelectedId={setSelectedId}
                                                         selectedHashtags={selectedHashtags}
                                                         selectedCluster={selectedCluster}
                                                         addHashtag={addHashtag}/>
                                        </TabPane>
                                        <TabPane tab="Explore districts" key={3}>
                                            <DistrictsTab selectedId={selectedId} setSelectedId={setSelectedId}
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
