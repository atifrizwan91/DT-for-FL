jsPlumb.ready(function () {
function termFreqMap(str) {
        var words = str.split(' ');
        var termFreq = {};
        words.forEach(function(w) {
            termFreq[w] = (termFreq[w] || 0) + 1;
        });
        return termFreq;
    }

    function addKeysToDict(map, dict) {
        for (var key in map) {
            dict[key] = true;
        }
    }

    function termFreqMapToVector(map, dict) {
        var termFreqVector = [];
        for (var term in dict) {
            termFreqVector.push(map[term] || 0);
        }
        return termFreqVector;
    }

    function vecDotProduct(vecA, vecB) {
        var product = 0;
        for (var i = 0; i < vecA.length; i++) {
            product += vecA[i] * vecB[i];
        }
        return product;
    }

    function vecMagnitude(vec) {
        var sum = 0;
        for (var i = 0; i < vec.length; i++) {
            sum += vec[i] * vec[i];
        }
        return Math.sqrt(sum);
    }

    function cosineSimilarity(vecA, vecB) {
        return vecDotProduct(vecA, vecB) / (vecMagnitude(vecA) * vecMagnitude(vecB));
    }

    Cosinesimilarity = function textCosineSimilarity(strA, strB) {
        var termFreqA = termFreqMap(strA);
        var termFreqB = termFreqMap(strB);

        var dict = {};
        addKeysToDict(termFreqA, dict);
        addKeysToDict(termFreqB, dict);

        var termFreqVecA = termFreqMapToVector(termFreqA, dict);
        var termFreqVecB = termFreqMapToVector(termFreqB, dict);

        return cosineSimilarity(termFreqVecA, termFreqVecB);
    }

    var instance = jsPlumb.getInstance({
        Connector: "Straight",
        PaintStyle: { strokeWidth: 3, stroke: "#ffa500", "dashstyle": "2 4" },
        Endpoint: [ "Dot", { radius: 5 } ],
        EndpointStyle: { fill: "#ffa500" },
        Container: "canvas"
    });

    window.jsp = instance;

    // get the two elements that contain a list inside them
    var list1El = document.querySelector(".gm-style-iw-a #list-one"),
        list2El = document.querySelector(".gm-style-iw-a #list-two"),
        list1Ul = list1El.querySelector("ul"),
        list2Ul = list2El.querySelector("ul");

    instance.draggable(list1El);
    instance.draggable(list2El);

    // get uls
    var lists = jsPlumb.getSelector("ul");

    // suspend drawing and initialise.
    instance.batch(function () {

        var selectedSources = [], selectedTargets = [];

        for (var l = 0; l < lists.length; l++) {

            var isSource = lists[l].getAttribute("source") != null,
                isTarget = lists[l].getAttribute("target") != null;

            // configure items
            var items = lists[l].querySelectorAll("li");
            for (var i = 0; i < items.length; i++) {

                if (isSource) {
instance.makeSource(items[i], {
                        allowLoopback: false,
                        anchor: ["Left", "Right" ]
                    });
                   /* if(items[i].innerHTML.toString()=='Body temperature VO')
                    {
                        


                    }

                    */




                        selectedSources.push(items[i]);



                }

                if (isTarget) {
                    instance.makeTarget(items[i], {
                        anchor: ["Left", "Right" ]
                    });
                   /* if (Math.random() < 0.2) {
                        */
                   selectedTargets.push(items[i]);
                   /*
                    }*/
                }
            }
        }

        var connCount = Math.max(selectedSources.length, selectedTargets.length);
        for (var i = 0; i < selectedTargets.length; i++) {
            for (var j = 0; j < selectedSources.length; j++) {
                var outputri = Cosinesimilarity(selectedSources[j].textContent.toLowerCase(), selectedTargets[i].textContent.toLowerCase());
                //alert(outputri);

                if (outputri > 0) {


                    instance.connect({source: selectedSources[j], target: selectedTargets[i]});
                }
            }
        }
    });

    var list1 = instance.addList(list2Ul);

    var list2 = instance.addList(list1Ul, {
        endpoint:["Rectangle", {width:20, height:20}]
    });


    instance.bind("click", function(c) { instance.deleteConnection(c); });

    jsPlumb.on(document, "change", "[type='checkbox']", function(e) {
        instance[e.srcElement.checked ? "addList" : "removeList"](e.srcElement.value === "list1" ? list1Ul : list2Ul);
    });

    jsPlumb.fire("jsPlumbDemoLoaded", instance);
});

