import { StatusBar } from 'expo-status-bar';
import {React,useState,useEffect} from 'react';
import { StyleSheet, Text, View,SafeAreaView, FlatList, TouchableOpacity, Modal, Image, Button } from 'react-native';
import ImageZoom from 'react-native-image-pan-zoom';
import axios from 'axios';

export default function App() {
  /*let data = [
          {key: 'Devin',imageurl:'https://upload.wikimedia.org/wikipedia/commons/e/ee/Sample_abc.jpg'},
          {key: 'Dan',imageurl:'https://sample-videos.com/img/Sample-jpg-image-1mb.jpg'},
          {key: 'Dominic',imageurl:'https://budgetstockphoto.com/samples/pics/dice.jpg'},
          {key: 'Jackson',imageurl:'https://res.cloudinary.com/demo/image/upload/sample.jpg'},
          {key: 'James',imageurl:'https://upload.wikimedia.org/wikipedia/commons/e/ee/Sample_abc.jpg'},
          {key: 'Joel',imageurl:'https://upload.wikimedia.org/wikipedia/commons/e/ee/Sample_abc.jpg'},
          {key: 'John',imageurl:'https://upload.wikimedia.org/wikipedia/commons/e/ee/Sample_abc.jpg'},
          {key: 'Jillian',imageurl:'https://upload.wikimedia.org/wikipedia/commons/e/ee/Sample_abc.jpg'},
          {key: 'Jimmy',imageurl:'https://upload.wikimedia.org/wikipedia/commons/e/ee/Sample_abc.jpg'},
          {key: 'Julie',imageurl:'https://upload.wikimedia.org/wikipedia/commons/e/ee/Sample_abc.jpg'},
        ];*/
  const [showModal,setshowModal] = useState(false);
  const [currimage,setCurrimage] = useState(false);
  const [data, setData] = useState([])
  
  useEffect(() => {
    
  axios.get('http://twilio-webhook-tva.herokuapp.com/getDatabase').then((response)=>{
	  //console.log(response.data.data)
	  setData(response.data.data)
	  console.log(data)
  });
  }, []);
  
  function onPressHandler(item){
	  console.log(item.imageurl)
	  setCurrimage(item.imageurl)
	  setshowModal(true)
  };
  function onclosePressHandler(){
	  setshowModal(false)
  };
  return (
    <SafeAreaView style={styles.container}>
	  <View style={{width:'100%',}}><Text style={styles.heading}>People Encountered</Text></View>
	  <View style = {styles.listview}>
      
	  <FlatList
	    style = {styles.listitems}
        data={data}
		ItemSeparatorComponent={
            () => <View style={{ height:20, backgroundColor: '#9ED9CCFF' }}/>
        }
		
        renderItem={({item}) => <TouchableOpacity onPress={()=>onPressHandler(item)}>
		<Text style={styles.item}>{item.key} on {item.date}</Text>
			
		</TouchableOpacity>}
		
      />
	  
	  
	  <Modal
			transparent={true}
			visible={showModal}
			style={{justifyContent:'center'}}
		>
		<View style={{backgroundColor:'rgba(0, 0, 0, 0.1)',flex:1}}>
			<View style={styles.modalStyle}>
			    <TouchableOpacity onPress={onclosePressHandler} style={{justifyContent:'center',textAlign:'right'}} ><Text style={{textAlign:'right'}}>X</Text></TouchableOpacity>
				<ImageZoom
				cropWidth='100%'
				cropHeight='100%'
				imageHeight={300}
				imageWidth={300}
				>
				
				<Image style={{width: '100%',height:'100%',resizeMode: 'contain',}} source={{uri:currimage}}></Image>
				</ImageZoom>
			</View>
		</View>
		</Modal>
	  
	  
	  </View>
      <StatusBar style="auto" />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#9ED9CCFF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  listitems: {
    flex: 2,
	height:20,
    //backgroundColor: '#FAA094FF',
	margin:20,
	
  },
  item:{
	  borderWidth:5,
	  borderColor:'#008C76FF',
	  backgroundColor: '#FAA094FF',
	  color:'#008C76FF',
	  fontWeight:"700",
	  padding:20,
	  textAlign:"center",
  },
  listview:{
	  flex: 1,
	  height:'100%',
	  width:'100%',
	  justifyContent: 'space-around',
  },
  heading:{
	  backgroundColor: '#36454F',
	  color:'#fff',
	  fontWeight:"700",
	  fontSize: 20,
	  textAlign:'center',
	  padding:20,
	  borderBottomEndRadius:20,
	  borderBottomStartRadius:20,
  },
  modalStyle:{
	  backgroundColor:"#FFFFFF",
	  margin:10,
	  marginTop:50,
	  padding:5,
	  
	  borderRadius:10,
	  height:'80%',
  }
});
