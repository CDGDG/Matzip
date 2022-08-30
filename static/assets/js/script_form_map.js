var mapContainer = document.getElementById('formmap'), // 지도를 표시할 div 
    mapOption = {
        center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    }; 

var marker = new daum.maps.Marker({
    position: new daum.maps.LatLng(37.537187, 127.005476),
    map: map
});

// 지도를 생성합니다    
var map = new kakao.maps.Map(mapContainer, mapOption);

// kakao 지도
var container = document.getElementById('formmap'); //지도를 담을 영역의 DOM 레퍼런스

function execDaumPostcode() {
	new daum.Postcode({
		oncomplete: function(data) {
			console.log(data)
			var addr = data.jibunAddress; // 최종 주소 변수

			// 주소 정보를 해당 필드에 넣는다.
			document.getElementById("id_address").value = addr;
			// 주소로 상세 정보를 검색
			$.ajax({
				url: `http://dapi.kakao.com/v2/local/search/address.json?query=${addr}&page=1&size=10`,
				type: "get",
				headers: {"Authorization": "KakaoAK 7988f17d47883052ebc22853ffe510c4"},
				success: function(results, status){
					if(status=="success"){
						var result = results.documents[0];
						// 해당 주소에 대한 좌표를 받아서
						var coords = new daum.maps.LatLng(result.address.y, result.address.x);
						map.relayout();
						// 지도 중심을 변경한다.
						map.setCenter(coords);
						// 마커를 결과값으로 받은 위치로 옮긴다.
						marker.setPosition(coords)
					}
				}
			})
		}
	}).open();
}

