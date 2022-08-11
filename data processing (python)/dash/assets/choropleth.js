window.choropleth = Object.assign({}, window.choropleth, {
    default: {
        StyleHandler: function(feature, context) {
            const {
                style,
            } = context.props.hideout;
            style.fillOpacity = feature.properties["opacity"];
            return style
        },
        PointToLayer: function(feature, latlng, context) {
            const id = feature.properties["id"];
            // const subtitle = feature.properties["subtitle"]

            var marker = L.marker(latlng, {
                icon: L.divIcon({
                    className: 'map-labels',   // Set class for CSS styling
                    html: '<div>' + id + '<div/>'
                    // html: '<div><b>' + id + '</b><br/><span>' + subtitle + '</span></div>'

                    // html: id
                }),
                zIndexOffset: 1000     // Make appear above other map features
            });
            return marker;
        },
        PointToLayerClusters: function(feature, latlng, context) {
            const id = feature.properties["id"];
            const size = feature.properties["size"];
            // const subtitle = feature.properties["subtitle"]

            return new L.CircleMarker(latlng, {radius: size*60}); 

            // }, 

            // var marker = L.marker(latlng, {
            //     icon: L.divIcon({
            //         className: 'circle',   // Set class for CSS styling
            //         html: '<div>Hello I am A Circle</div>'
            //         // html: '<div><b>' + id + '</b><br/><span>' + subtitle + '</span></div>'

            //         // html: id
            //     }),
            //     zIndexOffset: 1000     // Make appear above other map features
            // });
            // return marker;
        },
    }
});


// # style_handle = assign("""function(feature,context){
//     #     const {classes, colorscale, style, colorProp} = context.props.hideout;
//     #     const value = feature.properties[colorProp];
//     #     for (let i = 0; i < classes.length; ++i) {
//     #         if (value > classes[i]) {
//     #             style.fillColor=colorscale[i];
//     #         }
//     #     }
//     #     return style
//     # }""")