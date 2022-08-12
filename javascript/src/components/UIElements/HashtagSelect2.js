import { Input } from 'antd';
import React from 'react';
// const { Option } = Select;

const { Search } = Input;


const HashtagSelect2 = ({selectedHashtags, setSelectedHashtags}) => {
    let options = [];

    // for (let i = 0; i < children.length; i++) {
    //     options.push(<Option key={children[i]}>{children[i]}</Option>);
    // }

    // function onChange(hashtags) {
    //     setSelectedHashtags(hashtags)
    //     setUserCount()

    // }

    const addHashtag = (hashtag) => {
        if (hashtag.length > 0) {
            let newHashtags = [...selectedHashtags];
            newHashtags.push(hashtag)
            setSelectedHashtags(newHashtags);
        }
    }

    return (
        // <Select
        //     mode="tags"
        //     allowClear
        //     style={{
        //         width: '100%',
        //     }}
        //     placeholder="Search for hashtags"
        //     defaultValue={[]}
        //     onChange={setSelectedHashtags}
        //     value={selectedHashtags}
        // >
        //     {/*{options}*/}
        // </Select>

        <Search placeholder="Search for hashtags..." allowClear onSearch={addHashtag}  />

);
}

export default HashtagSelect2;