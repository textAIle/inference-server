import './App.css';
import logo from './logo.png';
import axios from "axios";
import { useEffect, useState } from "react";
import SimpleImageSlider from "react-simple-image-slider";

function App() {

    const fake = true

    const inferenceServer = "http://0.0.0.0:2224"
    const itemsBasePath = "data/items"

    const [images, setImages] = useState([
        { url: itemsBasePath + "1/1.jpeg" },
    ]);
    const [imageSlider, setImageSlider] = useState(
        <SimpleImageSlider
            width={800}
            height={600}
            images={images}
            showBullets={true}
            showNavs={true}
        />
    )
    const [attributes, setAttributes] = useState(itemsBasePath + "/1/attributes.json")
    const [labels, setLabels] = useState(<div>Initializing...</div>)
    const [pairIndicator, setPairIndicator] = useState("Initializing...")
    const [pairIndicatorColor, setPairIndicatorColor] = useState("black")
    const [size, setSize] = useState("Initializing...")
    const [color, setColor] = useState(<div className="color">Initializing...</div>)
    const [similarImages, setSimilarImages] = useState([<div>Initializing...</div>])

    function getImages() {
        axios({
            method: "GET",
            url: inferenceServer + "/getLatestImages",
        })
        .then((response) => {
            let imagePaths = response.data
            let imgs = []
            for (let key in imagePaths) {
                imgs.push(
                    { url: itemsBasePath + "/" + imagePaths[key] }
                )
            }
            console.log(imgs)
            setImageSlider(<div>Loading...</div>)
            setImages(imgs)
        }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    function getAttributes() {axios({
            method: "GET",
            url: inferenceServer + "/getLatestAttributes",
        })
        .then((response) => {
            let attributes = response.data
            console.log(itemsBasePath + "/" + attributes)
            setAttributes(itemsBasePath + "/" + attributes)
        }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    function getLabelDetection() {
        axios({
            method: "GET",
            url: inferenceServer + "/detectLabels",
        })
        .then((response) => {
            const labels = response.data
            let labelDivs = []
            for (let key in labels) {
                // let labelDiv = <div key={res[item]}>{item}</div>
                let labelDiv = <div key={labels[key]}>{key}<span>{labels[key]}</span></div>
                labelDivs.push(labelDiv)
            }
            setLabels(labelDivs)
        }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    function getLabelDetectionFake() {
        fetch(attributes)
            .then(function (response) {
                return response.json()
            })
            .then(function (json) {
                let labels = json["labels"]
                let labelDivs = []
                for (let key in labels) {
                    let val = labels[key]
                    for (let sub_key in val) {
                        let labelDiv = <div key={val[sub_key]}>{sub_key}<span>{val[sub_key]}</span></div>
                        labelDivs.push(labelDiv)
                    }
                }
                setLabels(labelDivs)
            });
    }

    function getObjectCount() {
        axios({
            method: "GET",
            url: inferenceServer + "/countObjects",
        })
        .then((response) => {
            const res = response.data
            console.log(res)
            const countTmp = parseInt(res)
            if (countTmp === 1) {
                setPairIndicator("Single shoe")
                setPairIndicatorColor("red")
            } else if (countTmp === 2) {
                setPairIndicator("Pair")
                setPairIndicatorColor("green")
            } else if (countTmp > 2) {
                setPairIndicator("More than two shoes")
                setPairIndicatorColor("red")
            } else {
                setPairIndicator("Error when counting shoes")
                setPairIndicatorColor("red")
            }
        }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    function getObjectCountFake() {
        fetch(attributes)
            .then(function (response) {
                return response.json()
            })
            .then(function (json) {
                let numShoes = json["numShoes"]
                let countTmp = parseInt(numShoes)
                if (countTmp === 1) {
                    setPairIndicator("Single shoe")
                    setPairIndicatorColor("red")
                } else if (countTmp === 2) {
                    setPairIndicator("Pair")
                    setPairIndicatorColor("green")
                } else if (countTmp > 2) {
                    setPairIndicator("More than two shoes")
                    setPairIndicatorColor("red")
                } else {
                    setPairIndicator("Error when counting shoes")
                    setPairIndicatorColor("red")
                }
            });
    }

    function getSizeFake() {
        fetch(attributes)
            .then(function (response) {
                return response.json()
            })
            .then(function (json) {
                let size = json["size"]
                setSize(size)
            });
    }

    function getColorFake() {
        fetch(attributes)
            .then(function (response) {
                return response.json()
            })
            .then(function (json) {
                let colors = json["color"]
                let colorSpans = []
                for (let key in colors) {
                    let colorSpan = <div key={colors[key]} className="color"><div style={{backgroundColor: colors[key]}}> </div><span>{colors[key]}</span></div>
                    colorSpans.push(colorSpan)
                }
                setColor(colorSpans)
            });
    }

    function getSimilarImages() {
        axios({
            method: "GET",
            url: inferenceServer + "/findSimilarImages",
        })
        .then((response) => {
            let imageUrls = response.data
            let imgs = []
            for (let key in imageUrls) {
                let img = <img src={imageUrls[key]} className="similar-image" />
                imgs.push(img)
            }
            setSimilarImages(imgs)
        }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    function getSimilarImagesFake() {
        fetch(attributes)
            .then(function (response) {
                return response.json()
            })
            .then(function (json) {
                let imageUrls = json["relatedImages"]
                let imgs = []
                for (let key in imageUrls) {
                    let img = <img src={imageUrls[key]} className="similar-image" />
                    imgs.push(img)
                }
                console.log(imgs)
                setSimilarImages(imgs)
            });
    }

    function updateInference() {
        console.log("Updating inference...");
        getImages()
        // getSimilarImages()
        if (fake) {
            getAttributes()
        } else {
            getLabelDetection()
            getObjectCount()
        }
    }
    useEffect(() => {
        console.log("use effect attributes")
        console.log(attributes)
        getLabelDetectionFake()
        getLabelDetectionFake()
        getObjectCountFake()
        getSizeFake()
        getColorFake()
        getSimilarImagesFake()
    }, [attributes])

    useEffect(() => {
        const updateStream = new EventSource(inferenceServer + "/streamUpdate")

        function handleStream(e) {
            console.log("Fetching inference update from directory...");
            console.log(e.data);
            updateInference();
        }
        updateStream.onmessage = e => {handleStream(e)}
        updateStream.onerror = e => {
            // gotcha - can close stream and "stall"
            // watch https://www.youtube.com/watch?v=rWIQLHp_JuU
            updateStream.close()
        }

        return () => {
            updateStream.close()
        }
    }, )

    useEffect( () => {
        setImageSlider(
            <SimpleImageSlider
                width={800}
                height={600}
                images={images}
                showBullets={true}
                showNavs={true}
            />
        )
    }, [images])

    function handleResell() {
        alert("Item has been labeled as resell.")
    }

    function handleRecycle() {
        alert("Item has been labeled as recyclable.")
    }

    function handleWaste() {
        alert("Item has been labeled as waste.")
    }

  return (
    <div className="App">
        <nav className="navbar">
            <div className="nav-container body-width">
                <img src={logo} />
                <h1 className="page-title">Textile Quality Assignment</h1>
                <div className="burger-menu">
                    <div></div>
                    <div></div>
                    <div></div>
                </div>
            </div>
        </nav>
        <section id="main" className="body-width">
            <div className="left-col">
                <div className="video-container">
                    {imageSlider}
                </div>
            </div>
            <div className="right-col">
                <div className="labels-container">
                    {labels}
                </div>
                <div className="details-container">
                    <span className="pair-indicator" style={{color: pairIndicatorColor}}>{pairIndicator}</span><br />
                    <b>Size: </b><span className="size">{size}</span><br />
                    <b>Color:</b>{color}<br />
                    <b>Reference images:</b>
                </div>
                <div className="ref-images-container">
                    {similarImages}
                </div>
                <div className="buttons-container">
                    <button onClick={handleResell}>Resell</button>
                    <button onClick={handleRecycle}>Recycle</button>
                    <button onClick={handleWaste}>Waste</button>
                </div>
            </div>
        </section>
        <footer>
            <div className="">
                <button className="start" onClick={updateInference}>></button>
            </div>
        </footer>
    </div>
  );
}

export default App;
