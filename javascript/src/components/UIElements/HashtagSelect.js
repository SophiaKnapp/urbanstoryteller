import {Select} from 'antd';
import React from 'react';
import top_hashtags_city from '../../assets/top_hashtags_city.json';
const { Option } = Select;

const HashtagSelect = ({addHashtag}) => {
    let options = [];

    const hashtags = top_hashtags_city.map((d) => d.hashtag);

    for (let i = 0; i < hashtags.length; i++) {
        options.push(<Option key={hashtags[i]}>{'#' + hashtags[i]}</Option>);
    }

    return (
        <Select
            showSearch
            optionFilterProp="children"
            style={{
                width: '100%',
            }}
            placeholder="Search for a hashtag..."
            defaultValue={[]}
            onChange={addHashtag}
        >
            {options}
        </Select>
    );
}

export default HashtagSelect;