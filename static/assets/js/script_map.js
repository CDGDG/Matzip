var lat
var lon
var map
var geocoder = new daum.maps.services.Geocoder();
var marker = new daum.maps.Marker({
	position: new daum.maps.LatLng(37.537187, 127.005476),
	map: map
});
var addr


// 현재 주소
function onGeoOk(position){
	lat = position.coords.latitude;
	lon = position.coords.longitude;
	// 위도 경도 받고

	var options = { //지도를 생성할 때 필요한 기본 옵션
		center: new kakao.maps.LatLng(lat, lon), //지도의 중심좌표.
		level: 3 //지도의 레벨(확대, 축소 정도)
	};

	map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴

	marker = new kakao.maps.Marker({
		map: map,
		title: "현재 위치",
		position: new kakao.maps.LatLng(lat, lon)
	});

	// 주소 얻기
	$.ajax({
		url: `https://dapi.kakao.com/v2/local/geo/coord2address?x=${lon}&y=${lat}`,
		type: "get",
		headers: {"Authorization": "KakaoAK 7988f17d47883052ebc22853ffe510c4"},
		success: function(result, status){
			if(result.documents && status == "success"){
				addr = !!result.documents[0].road_address?result.documents[0].road_address.address_name:result.documents[0].address.address_name.replace("서울", "서울특별시")
				$('#myaddr').text(addr)

				// 주변 식당 가져오기
				$.ajax({
					url: `/matzip/near/${addr.split(" ").slice(0, 2).join(" ")}/`,
					type: "get",
					success: function(results, status){
						if(status=='success'){
							for(let near of results.nears){
								c2a(near.address, near.name, near.id)
							}
						}
					}
				})
			}
		}
	})
	
}
function onGeoError(){
	alert("위치권한을 확인해주세요");
}

navigator.geolocation.getCurrentPosition(onGeoOk,onGeoError)


// kakao 지도
var container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스

function execDaumPostcode() {
	new daum.Postcode({
		oncomplete: function(data) {
			var addr = data.address; // 최종 주소 변수

			// 주소 정보를 해당 필드에 넣는다.
			document.getElementById("id_address").value = addr;
			// 주소로 상세 정보를 검색
			$.ajax({
				url: `http://dapi.kakao.com/v2/local/search/address.json?query=${data.address}&page=1&size=10`,
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


function c2a(addr_r, name_r, id_r){
	$.ajax({
		url: `http://dapi.kakao.com/v2/local/search/address.json?query=${addr_r.replace("서울특별시", "서울")}&page=1&size=10`,
		type: "get",
		headers: {"Authorization": "KakaoAK 7988f17d47883052ebc22853ffe510c4"},
		success: function(result, status){
			if(status == "success"){
				var coords_r = new kakao.maps.LatLng(result.documents[0].y, result.documents[0].x);
	
				// 결과값으로 받은 위치를 마커로 표시합니다
				var marker_r = new kakao.maps.Marker({
					map: map,
					position: coords_r,
					clickable: true,
					title: name_r,
				});

				kakao.maps.event.addListener(marker_r, "click", function(){
					location.href = `/matzip/detail/${id_r}/`
				})
			}
		}
	})
}
