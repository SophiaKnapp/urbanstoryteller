import {Input, Select} from 'antd';
import React from 'react';
// const { Option } = Select;

import top_hashtags_city from '../../assets/top_hashtags_city.json';


// const { Search } = Input;

const { Option } = Select;


const HashtagSelect = ({selectedHashtags, setSelectedHashtags}) => {
    let options = [];

    // for (let i = 0; i < children.length; i++) {
    //     options.push(<Option key={children[i]}>{children[i]}</Option>);
    // }

    // function onChange(hashtags) {
    //     setSelectedHashtags(hashtags)
    //     setUserCount()

    // }

    const hashtags = top_hashtags_city.map((d) => d.hashtag);
    console.log(hashtags);
    // hashtags.sort();

    for (let i = 0; i < hashtags.length; i++) {
        options.push(<Option key={hashtags[i]}>{hashtags[i]}</Option>);
        // options.push(<Option key={'test'+ i}>{'test'}</Option>);
    }


    const addHashtag = (hashtag) => {
        if (hashtag.length > 0) {
            let newHashtags = [...selectedHashtags];
            newHashtags.push(hashtag)
            setSelectedHashtags(newHashtags);
        }
    }

    return (
        <Select
            showSearch
            // mode="tags"
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