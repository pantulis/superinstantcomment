function canPlayAudioMP3(callback){
	try {
		var audio = new Audio();
		//Shortcut which doesn't work in Chrome (always returns ""); pass through
		// if "maybe" to do asynchronous check by loading MP3 data: URI
		if(audio.canPlayType('audio/mpeg; codecs="MPEG3"') == "probably") {
			callback(true);
			return;
		}

		//If this event fires, then MP3s can be played
		audio.addEventListener('canplaythrough', function(e){
			callback(true);
		}, false);

		//If this is fired, then client can't play MP3s
		audio.addEventListener('error', function(e){
			callback(false, this.error);
		}, false);

		//Smallest base64-encoded MP3 I could come up with (<0.000001 seconds long)
		audio.src = "data:audio/mpeg;base64,/+MYxAAAAANIAAAAAExBTUUzLjk4LjIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
		audio.load();
	}
	catch(e){
		callback(false, e);
	}
}