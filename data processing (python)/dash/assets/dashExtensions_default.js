window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            const {
                classes,
                colorscale,
                style,
                colorProp
            } = context.props.hideout;
            const value = feature.properties[colorProp];
            style.fillOpacity = feature.properties["opacity"];
            return style
        }
    }
});