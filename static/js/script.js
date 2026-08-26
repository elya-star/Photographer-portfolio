"use strict";

document.addEventListener("DOMContentLoaded",()=>{
initMobileMenu();
initBackToTop();
initHeroSlider();
initFeatureSlider();
initScrollReveal();
initPhotoLightbox();
initServiceGalleries();
initServiceReveal();
initCalendarSlider();
initDatesParallax();
initReviewExpand();
initReviewParallax();
});

function initMobileMenu(){
const toggle=document.querySelector(".menu-toggle");
const navigation=document.querySelector(".site-navigation");
const overlay=document.querySelector(".site-overlay");
const closeButton=document.querySelector("[data-menu-close]");

if(!toggle||!navigation||!overlay){
return;
}

function openMenu(){
navigation.classList.add("is-open");
overlay.classList.add("is-visible");
document.body.classList.add("is-locked");

toggle.setAttribute("aria-expanded","true");
navigation.setAttribute("aria-hidden","false");
}

function closeMenu(){
navigation.classList.remove("is-open");
overlay.classList.remove("is-visible");
document.body.classList.remove("is-locked");

toggle.setAttribute("aria-expanded","false");
navigation.setAttribute("aria-hidden","true");
}

toggle.addEventListener("click",()=>{
if(navigation.classList.contains("is-open")){
closeMenu();
}else{
openMenu();
}
});

closeButton?.addEventListener("click",closeMenu);
overlay.addEventListener("click",closeMenu);

navigation.querySelectorAll("a").forEach(link=>{
link.addEventListener("click",closeMenu);
});

document.addEventListener("keydown",event=>{
if(event.key==="Escape"&&navigation.classList.contains("is-open")){
closeMenu();
toggle.focus();
}
});

window.addEventListener("resize",()=>{
if(window.innerWidth>992){
closeMenu();
}
});
}

function initBackToTop(){
const button=document.querySelector(".back-to-top");

if(!button){
return;
}

function getScrollTop(){
return document.scrollingElement?.scrollTop||0;
}

function updateButton(){
const isVisible=getScrollTop()>300;

button.classList.toggle("is-visible",isVisible);
button.setAttribute(
"aria-hidden",
isVisible?"false":"true"
);
}

button.addEventListener("click",()=>{
document.scrollingElement?.scrollTo({
top:0,
left:0,
behavior:"smooth"
});
});

document.addEventListener(
"scroll",
updateButton,
{
passive:true,
capture:true
}
);

window.addEventListener(
"resize",
updateButton
);

updateButton();
}
function initHeroSlider(){
const slider=document.querySelector('[data-slider="hero"]');

if(!slider){
return;
}

const slides=Array.from(slider.querySelectorAll("[data-slide]"));
const dots=Array.from(slider.querySelectorAll("[data-slider-dot]"));
const previousButton=slider.querySelector("[data-slider-previous]");
const nextButton=slider.querySelector("[data-slider-next]");
const currentCounter=slider.querySelector("[data-slider-current]");
const totalCounter=slider.querySelector(
"[data-slider-total]"
);

if(totalCounter){
totalCounter.textContent=String(
slides.length
).padStart(2,"0");
}

if(slides.length===0){
return;
}

let currentIndex=0;
let autoplayId=null;
let pointerStartX=0;
let isPointerDown=false;

const autoplayDelay=5000;
const reduceMotion=window.matchMedia(
"(prefers-reduced-motion:reduce)"
).matches;

const normalizeIndex=index=>{
if(index<0){
return slides.length-1;
}

if(index>=slides.length){
return 0;
}

return index;
};

const formatNumber=number=>{
return String(number).padStart(2,"0");
};

const render=index=>{
currentIndex=normalizeIndex(index);

slides.forEach((slide,slideIndex)=>{
const active=slideIndex===currentIndex;

slide.classList.toggle("is-active",active);
slide.setAttribute("aria-hidden",active?"false":"true");
});


dots.forEach((dot,dotIndex)=>{
const active=dotIndex===currentIndex;

dot.classList.toggle("is-active",active);
dot.setAttribute("aria-selected",active?"true":"false");
});

if(currentCounter){
currentCounter.textContent=formatNumber(currentIndex+1);
}
};

const nextSlide=()=>{
render(currentIndex+1);
};

const previousSlide=()=>{
render(currentIndex-1);
};

const stopAutoplay=()=>{
if(autoplayId!==null){
window.clearInterval(autoplayId);
autoplayId=null;
}

slider.classList.remove("is-autoplaying");
};

const startAutoplay=()=>{
stopAutoplay();

if(slides.length<2||reduceMotion||document.hidden){
return;
}

slider.classList.add("is-autoplaying");

autoplayId=window.setInterval(()=>{
nextSlide();
},autoplayDelay);
};

const restartAutoplay=()=>{
startAutoplay();
};

previousButton?.addEventListener("click",()=>{
previousSlide();
restartAutoplay();
});

nextButton?.addEventListener("click",()=>{
nextSlide();
restartAutoplay();
});

dots.forEach(dot=>{
dot.addEventListener("click",()=>{
const index=Number(dot.dataset.sliderDot);

if(Number.isInteger(index)){
render(index);
restartAutoplay();
}
});
});

slider.addEventListener("mouseenter",stopAutoplay);
slider.addEventListener("mouseleave",startAutoplay);

slider.addEventListener("focusin",stopAutoplay);

slider.addEventListener("focusout",event=>{
if(!slider.contains(event.relatedTarget)){
startAutoplay();
}
});

slider.addEventListener("pointerdown",event=>{
isPointerDown=true;
pointerStartX=event.clientX;
});

slider.addEventListener("pointerup",event=>{
if(!isPointerDown){
return;
}

isPointerDown=false;

const distance=event.clientX-pointerStartX;

if(Math.abs(distance)<50){
return;
}

if(distance>0){
previousSlide();
}else{
nextSlide();
}

restartAutoplay();
});

slider.addEventListener("pointercancel",()=>{
isPointerDown=false;
});

document.addEventListener("visibilitychange",()=>{
if(document.hidden){
stopAutoplay();
}else{
startAutoplay();
}
});

render(0);
startAutoplay();
}

function initFeatureSlider(){
const slider=document.querySelector('[data-slider="features"]');

if(!slider){
return;
}

const slides=Array.from(
slider.querySelectorAll("[data-feature-slide]")
);
const dots=Array.from(
slider.querySelectorAll("[data-feature-dot]")
);
const previousButton=slider.querySelector(
"[data-feature-previous]"
);
const nextButton=slider.querySelector(
"[data-feature-next]"
);

if(slides.length<2){
return;
}

const AUTOPLAY_DELAY=4500;
const reducedMotion=window.matchMedia(
"(prefers-reduced-motion:reduce)"
).matches;

let currentIndex=0;
let autoplayId=null;
let pointerStartX=0;

function normalizeIndex(index){
if(index<0){
return slides.length-1;
}

if(index>=slides.length){
return 0;
}

return index;
}

function render(index){
currentIndex=normalizeIndex(index);

slides.forEach((slide,slideIndex)=>{
const active=slideIndex===currentIndex;

slide.classList.toggle("is-active",active);
slide.setAttribute(
"aria-hidden",
active?"false":"true"
);
});

dots.forEach((dot,dotIndex)=>{
dot.classList.toggle(
"is-active",
dotIndex===currentIndex
);
});

}

function nextSlide(){
render(currentIndex+1);
}

function previousSlide(){
render(currentIndex-1);
}

function stopAutoplay(){
if(autoplayId!==null){
window.clearInterval(autoplayId);
autoplayId=null;
}

slider.classList.remove("is-autoplaying");
}

function startAutoplay(){
stopAutoplay();

if(reducedMotion||document.hidden){
return;
}

slider.classList.add("is-autoplaying");

autoplayId=window.setInterval(
nextSlide,
AUTOPLAY_DELAY
);
}

function restartAutoplay(){
stopAutoplay();
startAutoplay();
}

previousButton?.addEventListener(
    "click",
    ()=>{
        previousSlide();
        restartAutoplay();
    }
);

nextButton?.addEventListener(
    "click",
    ()=>{
        nextSlide();
        restartAutoplay();
    }
);

dots.forEach(dot=>{
dot.addEventListener("click",()=>{
const index=Number(dot.dataset.featureDot);

if(Number.isInteger(index)){
render(index);
restartAutoplay();
}
});
});

slider.addEventListener("mouseenter",stopAutoplay);
slider.addEventListener("mouseleave",startAutoplay);
slider.addEventListener("focusin",stopAutoplay);

slider.addEventListener("focusout",event=>{
if(!slider.contains(event.relatedTarget)){
startAutoplay();
}
});

slider.addEventListener("pointerdown",event=>{
pointerStartX=event.clientX;
});

slider.addEventListener("pointerup",event=>{
const distance=event.clientX-pointerStartX;

if(Math.abs(distance)<50){
return;
}

if(distance>0){
previousSlide();
}else{
nextSlide();
}
});

document.addEventListener("visibilitychange",()=>{
if(document.hidden){
stopAutoplay();
}else{
startAutoplay();
}
});

render(0);
startAutoplay();
}

function initScrollReveal(){
const elements=document.querySelectorAll(
".portfolio-list-cta__container,.portfolio-list__header,.portfolio-category-card"
);

if(!elements.length){
return;
}

const reducedMotion=window.matchMedia(
"(prefers-reduced-motion:reduce)"
).matches;

if(reducedMotion){
elements.forEach(element=>{
element.classList.add("is-visible");
});
return;
}

const observer=new IntersectionObserver(entries=>{
entries.forEach(entry=>{
if(!entry.isIntersecting){
return;
}

entry.target.classList.add("is-visible");
observer.unobserve(entry.target);
});
},{
threshold:.14,
rootMargin:"0px 0px -8% 0px"
});

elements.forEach(element=>{
element.classList.add("reveal");
observer.observe(element);
});
}

function initPhotoLightbox(){
const lightbox=document.querySelector("[data-lightbox]");
const openButton=document.querySelector("[data-lightbox-open]");
const closeButton=document.querySelector("[data-lightbox-close]");
const viewport=document.querySelector("[data-lightbox-viewport]");
const content=document.querySelector("[data-lightbox-content]");
const image=document.querySelector("[data-lightbox-image]");
const title=document.querySelector("[data-lightbox-title]");
const currentCounter=document.querySelector("[data-lightbox-current]");
const totalCounter=document.querySelector("[data-lightbox-total]");
const previousButton=document.querySelector("[data-lightbox-previous]");
const nextButton=document.querySelector("[data-lightbox-next]");
const zoomInButton=document.querySelector("[data-lightbox-zoom-in]");
const zoomOutButton=document.querySelector("[data-lightbox-zoom-out]");
const resetButton=document.querySelector("[data-lightbox-reset]");
const zoomValue=document.querySelector("[data-lightbox-zoom-value]");
const themeButtons=Array.from(
document.querySelectorAll("[data-lightbox-theme]")
);
const galleryDataElement=document.getElementById(
"photo-gallery-data"
);

if(
!lightbox||
!openButton||
!closeButton||
!viewport||
!content||
!image||
!galleryDataElement
){
return;
}

let photos=[];

try{
photos=JSON.parse(galleryDataElement.textContent);
}catch(error){
console.error(
"Не удалось прочитать данные фотогалереи.",
error
);
return;
}

if(!Array.isArray(photos)||photos.length===0){
return;
}

const minScale=1;
const maxScale=4;
const scaleStep=.25;
const swipeDistance=55;

let currentIndex=Number(
lightbox.dataset.currentIndex||0
);
let scale=1;
let translateX=0;
let translateY=0;
let pointerStartX=0;
let pointerStartY=0;
let startTranslateX=0;
let startTranslateY=0;
let isDragging=false;
let previousFocus=null;
let pinchStartDistance=0;
let pinchStartScale=1;

function clamp(value,min,max){
return Math.min(
Math.max(value,min),
max
);
}

function normalizeIndex(index){
if(index<0){
return photos.length-1;
}

if(index>=photos.length){
return 0;
}

return index;
}

function updateTransform(){
if(scale<=1){
scale=1;
translateX=0;
translateY=0;
}else{
const imageWidth=image.clientWidth;
const imageHeight=image.clientHeight;

const maxX=Math.max(
0,
(imageWidth*scale-viewport.clientWidth)/2
);

const maxY=Math.max(
0,
(imageHeight*scale-viewport.clientHeight)/2
);

translateX=clamp(translateX,-maxX,maxX);
translateY=clamp(translateY,-maxY,maxY);
}

content.style.transform=(
`translate3d(${translateX}px,${translateY}px,0)`
);

image.style.transform=`scale(${scale})`;

viewport.classList.toggle("is-zoomed",scale>1);

if(zoomValue){
zoomValue.textContent=`${Math.round(scale*100)}%`;
}
}

function setScale(nextScale){
scale=clamp(
nextScale,
minScale,
maxScale
);

updateTransform();
}

function resetView(){
scale=1;
translateX=0;
translateY=0;
updateTransform();
}

function getTouchDistance(touches){
const first=touches[0];
const second=touches[1];

return Math.hypot(
second.clientX-first.clientX,
second.clientY-first.clientY
);
}

function renderPhoto(index){
currentIndex=normalizeIndex(index);

const item=photos[currentIndex];

resetView();

image.classList.add("is-changing");

window.setTimeout(()=>{
image.src=item.url;
image.alt=item.alt||item.title||"";

if(title){
title.textContent=item.title||"";
}

if(currentCounter){
currentCounter.textContent=String(
currentIndex+1
);
}

if(totalCounter){
totalCounter.textContent=String(
photos.length
);
}

image.classList.remove("is-changing");
},160);
}

function showPrevious(){
renderPhoto(currentIndex-1);
}

function showNext(){
renderPhoto(currentIndex+1);
}

function openLightbox(){
previousFocus=document.activeElement;

scale=1;
translateX=0;
translateY=0;

content.style.transform="translate3d(0,0,0)";
image.style.transform="scale(1)";

lightbox.classList.add("is-open");
lightbox.setAttribute("aria-hidden","false");
document.body.classList.add("lightbox-open");

requestAnimationFrame(()=>{
updateTransform();
});

closeButton.focus();
}

function closeLightbox(){
lightbox.classList.remove("is-open");
lightbox.setAttribute(
"aria-hidden",
"true"
);
document.body.classList.remove(
"lightbox-open"
);

resetView();

if(previousFocus instanceof HTMLElement){
previousFocus.focus();
}
}

function setTheme(theme){
lightbox.dataset.theme=theme;

themeButtons.forEach(button=>{
const active=(
button.dataset.lightboxTheme===theme
);

button.classList.toggle(
"is-active",
active
);

button.setAttribute(
"aria-pressed",
active?"true":"false"
);
});

try{
localStorage.setItem(
"photoLightboxTheme",
theme
);
}catch(error){
console.warn(
"Не удалось сохранить тему.",
error
);
}
}

openButton.addEventListener(
"click",
openLightbox
);

closeButton.addEventListener(
"click",
closeLightbox
);

previousButton?.addEventListener(
"click",
showPrevious
);

nextButton?.addEventListener(
"click",
showNext
);

zoomInButton?.addEventListener(
"click",
()=>{
setScale(scale+scaleStep);
}
);

zoomOutButton?.addEventListener(
"click",
()=>{
setScale(scale-scaleStep);
}
);

resetButton?.addEventListener(
"click",
resetView
);

themeButtons.forEach(button=>{
button.addEventListener("click",()=>{
setTheme(
button.dataset.lightboxTheme
);
});
});

viewport.addEventListener(
"wheel",
event=>{
if(!lightbox.classList.contains("is-open")){
return;
}

event.preventDefault();

const direction=event.deltaY<0?1:-1;

setScale(
scale+direction*scaleStep
);
},
{
passive:false
}
);

viewport.addEventListener(
"touchstart",
event=>{
if(event.touches.length!==2){
return;
}

event.preventDefault();

pinchStartDistance=getTouchDistance(event.touches);
pinchStartScale=scale;
},
{
passive:false
}
);

viewport.addEventListener(
"touchmove",
event=>{
if(event.touches.length!==2||pinchStartDistance<=0){
return;
}

event.preventDefault();

const currentDistance=getTouchDistance(event.touches);
const ratio=currentDistance/pinchStartDistance;

scale=clamp(
pinchStartScale*ratio,
minScale,
maxScale
);

updateTransform();
},
{
passive:false
}
);

viewport.addEventListener(
"touchend",
event=>{
if(event.touches.length<2){
pinchStartDistance=0;
pinchStartScale=scale;
}
},
{
passive:true
}
);

viewport.addEventListener(
"dblclick",
()=>{
if(scale===1){
setScale(2);
}else{
resetView();
}
}
);

viewport.addEventListener(
"pointerdown",
event=>{
pointerStartX=event.clientX;
pointerStartY=event.clientY;

if(scale<=1){
return;
}

isDragging=true;
startTranslateX=translateX;
startTranslateY=translateY;

viewport.classList.add(
"is-dragging"
);

viewport.setPointerCapture(
event.pointerId
);
}
);

viewport.addEventListener(
"pointermove",
event=>{
if(!isDragging){
return;
}

translateX=(
startTranslateX+
event.clientX-
pointerStartX
);

translateY=(
startTranslateY+
event.clientY-
pointerStartY
);

updateTransform();
}
);

function stopDragging(event){
if(!isDragging){
return;
}

isDragging=false;

viewport.classList.remove(
"is-dragging"
);

if(
event.pointerId!==undefined&&
viewport.hasPointerCapture(event.pointerId)
){
viewport.releasePointerCapture(
event.pointerId
);
}
}

viewport.addEventListener(
"pointerup",
event=>{
if(scale===1){
const distanceX=(
event.clientX-
pointerStartX
);

const distanceY=(
event.clientY-
pointerStartY
);

if(
Math.abs(distanceX)>swipeDistance&&
Math.abs(distanceX)>Math.abs(distanceY)
){
if(distanceX>0){
showPrevious();
}else{
showNext();
}
}
}

stopDragging(event);
}
);

viewport.addEventListener(
"pointercancel",
stopDragging
);

document.addEventListener(
"keydown",
event=>{
if(!lightbox.classList.contains("is-open")){
return;
}

if(event.key==="Escape"){
closeLightbox();
}

if(event.key==="ArrowLeft"){
showPrevious();
}

if(event.key==="ArrowRight"){
showNext();
}

if(event.key==="+"||event.key==="="){
setScale(scale+scaleStep);
}

if(event.key==="-"){
setScale(scale-scaleStep);
}

if(event.key==="0"){
resetView();
}
}
);

let savedTheme="dark";

try{
savedTheme=(
localStorage.getItem(
"photoLightboxTheme"
)||"dark"
);
}catch(error){
savedTheme="dark";
}

if(
!["dark","gray","light"].includes(
savedTheme
)
){
savedTheme="dark";
}

setTheme(savedTheme);
updateTransform();
}

function initServiceGalleries(){
    const galleries = document.querySelectorAll(
        "[data-service-gallery]"
    );

    if(!galleries.length){
        return;
    }

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    galleries.forEach(gallery=>{
        const slides = [
            ...gallery.querySelectorAll(
                "[data-service-slide]"
            )
        ];

        const previousButton = gallery.querySelector(
            "[data-service-prev]"
        );

        const nextButton = gallery.querySelector(
            "[data-service-next]"
        );

        const currentCounter = gallery.querySelector(
            "[data-service-current]"
        );

        const totalCounter = gallery.querySelector(
            "[data-service-total]"
        );

        if(slides.length === 0){
            return;
        }

        let currentIndex = 0;
        let autoplayTimer = null;
        let touchStartX = 0;

        const autoplayDelay = 4000;

        function showSlide(index){
            currentIndex =
                (index + slides.length) % slides.length;

            slides.forEach((slide,slideIndex)=>{
                const active =
                    slideIndex === currentIndex;

                slide.classList.toggle(
                    "is-active",
                    active
                );

                slide.setAttribute(
                    "aria-hidden",
                    active ? "false" : "true"
                );
            });

            if(currentCounter){
                currentCounter.textContent =
                    String(currentIndex + 1)
                        .padStart(2,"0");
            }
        }

        function stopAutoplay(){
            if(!autoplayTimer){
                return;
            }

            clearInterval(autoplayTimer);
            autoplayTimer = null;
        }

        function startAutoplay(){
            stopAutoplay();

            if(
                reducedMotion.matches ||
                slides.length <= 1
            ){
                return;
            }

            autoplayTimer = setInterval(()=>{
                showSlide(currentIndex + 1);
            },autoplayDelay);
        }

        function restartAutoplay(){
            stopAutoplay();
            startAutoplay();
        }

        if(totalCounter){
            totalCounter.textContent =
                String(slides.length)
                    .padStart(2,"0");
        }

        previousButton?.addEventListener(
            "click",
            ()=>{
                showSlide(currentIndex - 1);
                restartAutoplay();
            }
        );

        nextButton?.addEventListener(
            "click",
            ()=>{
                showSlide(currentIndex + 1);
                restartAutoplay();
            }
        );

        gallery.addEventListener(
            "mouseenter",
            stopAutoplay
        );

        gallery.addEventListener(
            "mouseleave",
            startAutoplay
        );

        gallery.addEventListener(
            "touchstart",
            event=>{
                touchStartX =
                    event.changedTouches[0]
                        .clientX;

                stopAutoplay();
            },
            {
                passive:true
            }
        );

        gallery.addEventListener(
            "touchend",
            event=>{
                const touchEndX =
                    event.changedTouches[0]
                        .clientX;

                const distance =
                    touchEndX - touchStartX;

                if(Math.abs(distance) >= 50){
                    if(distance < 0){
                        showSlide(
                            currentIndex + 1
                        );
                    }else{
                        showSlide(
                            currentIndex - 1
                        );
                    }
                }

                startAutoplay();
            },
            {
                passive:true
            }
        );

        showSlide(0);
        startAutoplay();
    });
}


function initServiceReveal(){
    const sections = [
        ...document.querySelectorAll(
            ".service-section"
        )
    ];

    if(!sections.length){
        return;
    }

    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        );

    if(reducedMotion.matches){
        sections.forEach(section=>{
            section.classList.add("is-visible");
        });

        return;
    }

    sections.forEach((section,index)=>{
        section.style.setProperty(
            "--service-reveal-delay",
            `${Math.min(index * 90, 360)}ms`
        );
    });

    const observer = new IntersectionObserver(
        entries=>{
            entries.forEach(entry=>{
                if(!entry.isIntersecting){
                    return;
                }

                entry.target.classList.add(
                    "is-visible"
                );

                observer.unobserve(
                    entry.target
                );
            });
        },
        {
            threshold:0.15,
            rootMargin:"0px 0px -8% 0px"
        }
    );

    sections.forEach(section=>{
        observer.observe(section);
    });
}

function initCalendarSlider(){
const slider=document.querySelector("[data-calendar-slider]");

if(!slider){
return;
}

const months=[
...slider.querySelectorAll("[data-calendar-month]")
];

const titles=[
...slider.querySelectorAll("[data-calendar-title]")
];

const dots=[
...slider.querySelectorAll("[data-calendar-dot]")
];

const previousButton=slider.querySelector(
"[data-calendar-previous]"
);

const nextButton=slider.querySelector(
"[data-calendar-next]"
);

const viewport=slider.querySelector(
".dates-calendar-viewport"
);

if(!months.length){
return;
}

let currentIndex=0;
let touchStartX=0;
let resizeFrame=null;

function clampIndex(index){
return Math.max(
0,
Math.min(index,months.length-1)
);
}

function updateViewportHeight(){
if(!viewport){
return;
}

const activeMonth=months[currentIndex];

if(!activeMonth){
return;
}

const activeHeight=activeMonth.offsetHeight;

if(activeHeight>0){
viewport.style.height=`${activeHeight}px`;
}
}

function showMonth(index){
const safeIndex=clampIndex(index);

currentIndex=safeIndex;

months.forEach((month,monthIndex)=>{
const isActive=monthIndex===currentIndex;

month.classList.toggle(
"is-active",
isActive
);

month.setAttribute(
"aria-hidden",
isActive?"false":"true"
);

month.querySelectorAll(
"a,button,input,select,textarea"
).forEach(element=>{
element.tabIndex=isActive?0:-1;
});
});

titles.forEach((title,titleIndex)=>{
title.classList.toggle(
"is-active",
titleIndex===currentIndex
);
});

dots.forEach((dot,dotIndex)=>{
const isActive=dotIndex===currentIndex;

dot.classList.toggle(
"is-active",
isActive
);

dot.setAttribute(
"aria-selected",
isActive?"true":"false"
);

dot.tabIndex=isActive?0:-1;
});

if(previousButton){
previousButton.disabled=currentIndex===0;
}

if(nextButton){
nextButton.disabled=(
currentIndex===months.length-1
);
}

window.requestAnimationFrame(()=>{
updateViewportHeight();
});
}

previousButton?.addEventListener(
"click",
()=>{
showMonth(currentIndex-1);
}
);

nextButton?.addEventListener(
"click",
()=>{
showMonth(currentIndex+1);
}
);

dots.forEach((dot,index)=>{
dot.addEventListener(
"click",
()=>{
showMonth(index);
}
);
});

slider.addEventListener(
"keydown",
event=>{
if(event.key==="ArrowLeft"){
event.preventDefault();
showMonth(currentIndex-1);
}

if(event.key==="ArrowRight"){
event.preventDefault();
showMonth(currentIndex+1);
}

if(event.key==="Home"){
event.preventDefault();
showMonth(0);
}

if(event.key==="End"){
event.preventDefault();
showMonth(months.length-1);
}
}
);

slider.addEventListener(
"touchstart",
event=>{
if(!event.changedTouches.length){
return;
}

touchStartX=event.changedTouches[0].clientX;
},
{
passive:true
}
);

slider.addEventListener(
"touchend",
event=>{
if(!event.changedTouches.length){
return;
}

const touchEndX=(
event.changedTouches[0].clientX
);

const distance=touchEndX-touchStartX;

if(Math.abs(distance)<50){
return;
}

if(distance<0){
showMonth(currentIndex+1);
}else{
showMonth(currentIndex-1);
}
},
{
passive:true
}
);

window.addEventListener(
"resize",
()=>{
if(resizeFrame!==null){
window.cancelAnimationFrame(
resizeFrame
);
}

resizeFrame=window.requestAnimationFrame(
()=>{
resizeFrame=null;
updateViewportHeight();
}
);
}
);

if("ResizeObserver" in window){
const resizeObserver=new ResizeObserver(()=>{
updateViewportHeight();
});

months.forEach(month=>{
resizeObserver.observe(month);
});
}

showMonth(0);
}

function initReviewExpand(){
    const reviews = document.querySelectorAll(
        ".review-story"
    );

    if(!reviews.length){
        return;
    }

    reviews.forEach(review=>{
        const text = review.querySelector(
            "[data-review-text]"
        );

        const button = review.querySelector(
            "[data-review-more]"
        );

        if(!text || !button){
            return;
        }

        requestAnimationFrame(()=>{
            const needsExpansion =
                text.scrollHeight >
                text.clientHeight + 4;

            if(!needsExpansion){
                return;
            }

            button.hidden = false;
        });

        button.addEventListener(
            "click",
            ()=>{
                const expanded =
                    text.classList.toggle(
                        "is-expanded"
                    );

                button.classList.toggle(
                    "is-expanded",
                    expanded
                );

                button.childNodes[0].textContent =
                    expanded
                        ? "Свернуть "
                        : "Читать полностью ";
            }
        );
    });
}

function initReviewParallax(){
    const section = document.querySelector(
        "[data-review-parallax]"
    );

    if(!section){
        return;
    }

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if(reducedMotion){
        return;
    }

    let ticking = false;

    function updateParallax(){
        const rect = section.getBoundingClientRect();
        const viewportHeight = window.innerHeight;

        if(
            rect.bottom <= 0 ||
            rect.top >= viewportHeight
        ){
            ticking = false;
            return;
        }

        const sectionCenter =
            rect.top + rect.height / 2;

        const viewportCenter =
            viewportHeight / 2;

        const distance =
            sectionCenter - viewportCenter;

        const offset = Math.max(
            -150,
            Math.min(
                150,
                distance * -0.24
            )
        );

        section.style.setProperty(
            "--review-parallax",
            `${offset}px`
        );

        ticking = false;
    }

    function requestParallaxUpdate(){
        if(ticking){
            return;
        }

        ticking = true;

        requestAnimationFrame(
            updateParallax
        );
    }

    window.addEventListener(
        "scroll",
        requestParallaxUpdate,
        {passive:true}
    );

    window.addEventListener(
        "resize",
        requestParallaxUpdate
    );

    updateParallax();
}

function initDatesParallax(){
    const section = document.querySelector(
        "[data-dates-parallax]"
    );

    if(!section){
        return;
    }

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if(reducedMotion){
        return;
    }

    let ticking = false;

    function update(){
        const rect = section.getBoundingClientRect();
        const viewportHeight = window.innerHeight;

        if(
            rect.bottom <= 0 ||
            rect.top >= viewportHeight
        ){
            ticking = false;
            return;
        }

        const sectionCenter =
            rect.top + rect.height / 2;

        const viewportCenter =
            viewportHeight / 2;

        const distance =
            sectionCenter - viewportCenter;

        const offset = Math.max(
            -150,
            Math.min(
                150,
                distance * -0.40
            )
        );

        section.style.setProperty(
            "--dates-parallax",
            `${offset}px`
        );

        ticking = false;
    }

    function requestUpdate(){
        if(ticking){
            return;
        }

        ticking = true;

        requestAnimationFrame(update);
    }

    window.addEventListener(
        "scroll",
        requestUpdate,
        {passive:true}
    );

    window.addEventListener(
        "resize",
        requestUpdate
    );

    update();
}