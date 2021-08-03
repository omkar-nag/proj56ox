document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#linkallposts').addEventListener('click', () => showposts('all'));
    if (!document.querySelector('#newpost')) {
        var misc1=document.createElement('div')
        misc1.id='newpost'
        var misc2=document.createElement('div')
        misc2.id='newpostdiv'
        var misc3=document.createElement('div')
        misc3.id='myprofile'
        var misc4=document.createElement('div')
        misc4.id='logout'
        var misc5=document.createElement('div')
        misc5.id='followingtab'
        document.querySelector("#everything").appendChild(misc1)
        document.querySelector("#everything").appendChild(misc2)
        document.querySelector("#everything").appendChild(misc3)
        document.querySelector("#everything").appendChild(misc4)
        document.querySelector("#everything").appendChild(misc5)
    }
    document.querySelector("#followingtab").addEventListener('click',() => showposts('following'));
    document.querySelector('#newpost').addEventListener('click',() => makepost());
    document.querySelector("#myprofile").addEventListener('click', () => follower(name))
    var name=document.querySelector('#myprofile').innerHTML;
    document.querySelector("#logout").addEventListener('click',() => showposts('all'));
    
    showposts('all');

});

//  SHOW THE POSTS REQUESTED

function showposts(param)

{
    document.getElementById("pagination").style.display='block';

    if (param=='all') {
        
        document.getElementById("profile_page").style.display="none";
        document.querySelector("#alltheposts").textContent='';
        var head=document.createElement('div');
        head.innerHTML="All posts"
        document.querySelector("#alltheposts").appendChild(head);
        head.classList.add("sticky");
    }
    else if (param=='following') {
        document.getElementById("profile_page").style.display="none";
        document.querySelector("#alltheposts").textContent='';
        var head=document.createElement('div');
        head.innerHTML="Accounts You Follow"
        document.querySelector("#alltheposts").appendChild(head);
        head.classList.add("sticky");
    }
    else {
        document.getElementById("profile_page").style.display="block";
        document.querySelector("#alltheposts").textContent='';
        var head=document.createElement('div');
        head.innerHTML=`@${param}`
        document.querySelector("#alltheposts").appendChild(head);
        head.classList.add("sticky");

    }
    
    var hr=document.createElement("hr")
    hr.style.width='40ch'
    hr.style.marginLeft='15px'
    hr.style.fontWeight='2ch'
    document.querySelector("#alltheposts").appendChild(hr);
    document.getElementById("alltheposts").style.display='block';
    document.getElementById("newpostdiv").style.display="none";

    
    var count=0;
    var currentpage=0
    

    fetch(`/posts/${param}`)
    .then(response => response.json())
    .then(posts => {

        var myuser=posts.user
        posts.postarray.forEach(post => {
          
            // content of the post
            
            var userelem=document.createElement('a');
            var textelem=document.createElement('p');
            var timeelem=document.createElement('p');
            var divelem=document.createElement('div');
            var like=document.createElement("p");
            like.id=post.id;
            
            var pic = document.createElement('button')
            if (post.user!==myuser) {
                fetch(`/like/${post.id}`, {
                    method: 'GET'
                })
                .then(response => response.json())
                .then(likes => {
                    if (likes.liked) {
                        like.innerHTML=`<i style='color: red;' class="fas fa-heart"></i> ${likes.likes}`
                    }
                    else {
                        like.innerHTML=`<i style='color: red;' class="far fa-heart"></i> ${likes.likes}`
                    }

                })
            }    
            if (myuser==`${post.user}` && param!="all"){
                var edit = document.createElement('a')
                edit.innerHTML='Edit'
            }
            userelem.innerHTML=`${post.user}`
            textelem.innerHTML=`${post.text}`
            var time = post.timestamp
            var d = new Date(time);
            d.setHours(d.getHours() + 5);
            d.setMinutes(d.getMinutes() + 30);
            timeelem.innerHTML = d.toString().slice(4,10) + d.toString().slice(15,21);
            pic.innerHTML=`${userelem.innerHTML.slice(0,1).toUpperCase()}`
            
            // merging them into a single div and appending to the main div

            userelem.setAttribute("href","#")
            userelem.addEventListener('click', () => {
                follower(post.user);
              });
            divelem.appendChild(pic)
            divelem.append(userelem)
            divelem.appendChild(textelem)
            divelem.appendChild(timeelem)
            divelem.appendChild(like)
            if (edit) {
                divelem.appendChild(edit)
                edit.classList.add('edit');
                edit.onclick=()=>{
                    edit.parentNode.removeChild(edit);
                    textelem.parentNode.removeChild(textelem);
                    timeelem.parentNode.removeChild(timeelem);
                    like.parentNode.removeChild(like);
                    var area=document.createElement('textarea')
                    area.value=`${post.text}`
                    area.classList.add('textarea1');
                    area.style.height='200px'
                    area.style.fontSize='15px'
                    area.style.borderColor='rgb(240, 240, 240)'
                    area.style.backgroundColor='white'
                    var btn=document.createElement('button')
                    btn.classList.add('submitpost');
                    btn.style.fontSize='12px'
                    btn.style.marginLeft='0px'
                    btn.innerHTML="Update"
                    divelem.appendChild(area)
                    divelem.appendChild(btn)
                    // starts here
                    btn.onclick= function() {
                        const text = area.value
                        if (area.value=='') {
                            alert("Post cannot be empty!")
                        }
                        else {
                            fetch('/create',{
                                method: 'PUT',
                                body: JSON.stringify({
                                    text: text,
                                    id: `${post.id}`
                                })
                            })
                            .then(response=>response.json())
                            .then(result => {
                                setTimeout(function() {
                                    btn.parentNode.removeChild(btn);
                                    area.parentNode.removeChild(area);
                                    divelem.append(userelem)
                                    textelem.innerHTML=area.value
                                    divelem.appendChild(textelem)
                                    divelem.appendChild(timeelem)
                                    divelem.appendChild(like)
                                    divelem.appendChild(edit)
                                 }, 200)
                            });
                        return false;
                        }; 
                    }                    
                }
                // ends here
            }
            like.onclick=() => {
                likefunc(post.id)
            }
            divelem.classList.add('postdiv');
            userelem.classList.add('poster');
            textelem.classList.add('posttext');
            timeelem.classList.add('time');
            like.classList.add('like');
            pic.classList.add('pic')
            
            
            const currentid= Math.floor(count/10);
            if (count%10===0) {
                var paginateddiv=document.createElement('div')
                paginateddiv.id=`page${currentid}`;
                document.getElementById(`alltheposts`).appendChild(paginateddiv)
                document.getElementById(`page${currentid}`).appendChild(divelem)
            }
            else {
                document.getElementById(`page${currentid}`).appendChild(divelem)
            }

            count++;
        });
        document.getElementById('cpage').innerHTML=1

        var c = document.getElementById("alltheposts").childElementCount - 2;
        for (i = 0; i < c; i++) {
            document.getElementById(`page${i}`).style.display='none';
            
        }
        document.getElementById(`page${currentpage}`).style.display='block'
        document.getElementById("nextpage").addEventListener('click',() => {
            var npage=currentpage+1
            var c = document.getElementById("alltheposts").childElementCount - 2;
            
            if (npage<c) {
                document.getElementById(`page${currentpage}`).style.display='none'
                document.getElementById(`page${npage}`).style.display='block'
                document.getElementById('cpage').innerHTML=currentpage+2
                currentpage++
                        
            }
            
        })
        document.getElementById("prevpage").addEventListener('click',() => {
            var ppage=currentpage-1
            var c = document.getElementById("alltheposts").childElementCount - 2;
            if (ppage>-1){
                document.getElementById(`page${currentpage}`).style.display='none'
                document.getElementById(`page${ppage}`).style.display='block'
                document.getElementById('cpage').innerHTML=currentpage
                currentpage--
            }
            
        })
            
    })

};


// CREATE NEW POST

function makepost() {
    document.getElementById("pagination").style.display='none';

    document.getElementById("alltheposts").style.display='none';
    document.getElementById("newpostdiv").style.display="block";
    document.getElementById("profile_page").style.display="none";
    var btn=document.getElementById("submitpost")
    
    btn.onclick= function() {
        const text = document.querySelector('#textarea1').value;
        if (document.getElementById("textarea1").value=='') {
            alert("Post cannot be empty!")
        }
        else {
            fetch('/create', {
                method: 'POST',
                body: JSON.stringify({
                    text: text
                })
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            });
            setTimeout(function() { showposts('all'); }, 200)
            document.querySelector('#textarea1').value='';
            return false;
        };       
    }
    
};       
        
// USER PROFILE

function follower(user) {
    
    if (document.getElementById("myprofile").innerHTML!=='') {
        document.getElementById("alltheposts").style.display='none';
        document.getElementById("newpostdiv").style.display="none";
        document.getElementById("profile_page").style.display="block";
        fetch(`/profile/${user}`)
        .then(response => response.json())
        .then(followers => {
            document.getElementById("followerscount").innerHTML=followers.follower_count
            document.getElementById("followingcount").innerHTML=followers.following_count
            if (followers.visiter === user) {
                document.getElementById("followbutton").hidden=true;
            }
            else {
                document.getElementById("followbutton").hidden=false;
                if(!followers['isfollowing']) {
                    document.getElementById("followbutton").innerHTML='Follow'
                }
                else document.getElementById("followbutton").innerHTML='Unfollow'
                document.getElementById("followbutton").onclick= () =>{
                   follow(`${user}`);                
                }
            }
            showposts(user);
        });
    }
    else {
        document.getElementById("demo").innerHTML = "Login to continue";
        setTimeout(function() {
              $('#demo').html('');
        }, 2000);
    }
}


// FOLLOW A USER 


function follow(target) {
    
    fetch(`/follow/${target}`, {
        method: 'POST',
        body: JSON.stringify({
            target: target
        })
        })
        .then(response => response.json())
        .then(result => {
            if (result['followed']) {
                document.getElementById("followbutton").innerHTML='Unfollow'
            }
            else document.getElementById("followbutton").innerHTML='Follow'
        });
        
        setTimeout(function() { 
            fetch(`/profile/${target}`)
            .then(response => response.json())
            .then(followers => {
            document.getElementById("followerscount").innerHTML=followers.follower_count
            document.getElementById("followingcount").innerHTML=followers.following_count
        })
    }, 100)    
}

function likefunc(postid) {
    fetch(`/like/${postid}`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(likes =>{
        if (likes.liked) {
            document.getElementById(postid).innerHTML=`<i style='color: red;' class="fas fa-heart"></i> ${likes.likes}`
        }
        else {
            document.getElementById(postid).innerHTML=`<i style='color: red;' class="far fa-heart"></i> ${likes.likes}`
        }
    })
}