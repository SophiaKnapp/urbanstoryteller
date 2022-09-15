import React from 'react';
import '../../../App.css';
import {Texts} from "../../../assets/texts";
import HashtagSelect from "./HashtagSelect";
import HashtagsChart from "./HashtagsChart";

const HashtagsTab = ({selectedId, setSelectedId, selectedHashtags, addHashtag, countsPerQuarter, selectedCluster, max}) => {
    return (
            <div className='sider-card'>
                <HashtagSelect addHashtag={addHashtag}/>
                {selectedHashtags.length > 0 || selectedCluster ? (
                        <HashtagsChart countsPerQuarter={countsPerQuarter} max={max} selectedId={selectedId} setSelectedId={setSelectedId} selectedHashtags={selectedHashtags} selectedCluster={selectedCluster} ></HashtagsChart>
                    ) :
                    (
                        <div>
                            <br/>
                            <div><b>{Texts.selectAHashtag}</b></div>
                        </div>
                    )
                }
            </div>
    )
}
export default HashtagsTab;