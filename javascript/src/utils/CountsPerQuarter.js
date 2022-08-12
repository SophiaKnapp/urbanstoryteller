import React from "react";

import posts_users_stories from '../assets/posts_users_stories.json';
import getCount from "../assets/hashtag_frequencies";

const CountsPerQuarter = (selectedHashtags, selectedCluster) => {
    const values = [];
    const potatoes = posts_users_stories.map((d) => d.quarter);
    let allHashtags = selectedHashtags;
    if (selectedCluster) {
        allHashtags = selectedHashtags.concat(selectedCluster.hashtags);
    }

    potatoes.map((id) => {
        const json = getCount(id);
        const totalCount = json[id];

        let selectedHashtagsCount = 0;
        if (allHashtags.length > 0) {
            for (let j = 0; j < allHashtags.length; j++) {
                let hashtag = allHashtags[j];
                const count = json[hashtag];
                if (count !== undefined) {
                    selectedHashtagsCount += count;
                }
            }
        }
        values[id] = {
            "totalCount" : totalCount,
            "count" : allHashtags.length === 0 ? totalCount : selectedHashtagsCount,
            "relativeAmount": selectedHashtagsCount / totalCount
        }
    })
    return values;
}
export default CountsPerQuarter;