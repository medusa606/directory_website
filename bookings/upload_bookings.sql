-- Booking/delivery URL bulk update
-- Generated from bookings/listings_with_bookings.csv

ALTER TABLE public.listings DISABLE TRIGGER trg_listings_audit;

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/nala-not-just-noodles-bristol'
WHERE id = '009046d3-d2e8-436e-980d-dabb6de03719';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/harbour-hub',
  booking_resdiary = 'https://dishcult.com/restaurant/iontheharbour?sortOrder=0&page=1&bookingDate=2024-03-28&covers=2&promotionId=0&bookingTime=19:30'
WHERE id = '01517ec3-b3b8-475f-80f9-21813ef7cd20';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/co-op-horfield-filton-road/iCh-sejDUfW9YuskWCuneA'
WHERE id = '018379ff-0e74-4c0f-988f-a1dc74af4b04';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/vice?sortOrder=0&page=1'
WHERE id = '0197f0c2-3029-428d-9494-d12cde19d37e';

UPDATE public.listings SET
  booking_resdiary = 'https://www.resdiary.com/restaurant/pizzabianchi'
WHERE id = '01b7ab94-46a9-46a9-b731-ed933cb39fec';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/clifton/the-lost-found-bristol'
WHERE id = '02600ea9-b9a3-459d-8b2b-927c3635dcf2';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '032bdcf9-0807-49d1-9031-b2284e7d8ad0';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '0333dfa9-7290-44a4-a310-35af1e01bbdb';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/mowgli-bristol'
WHERE id = '03cc2b3a-5013-4061-9ce3-020045d2515a';

UPDATE public.listings SET
  booking_resdiary = 'https://booking.resdiary.com/widget/Standard/TheGreyhoundInn/58622'
WHERE id = '0426de78-4287-44e3-8236-1c81c607a4ab';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/pizzarova/85V81zm0V5-RmlcSMWef0w'
WHERE id = '042d1821-8af7-4aa1-85bd-412ed56f42f0';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/brunel-raj'
WHERE id = '0436f573-ffee-4b4f-b699-e695215d2c4f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/horangeepocha'
WHERE id = '0442f4f2-6b80-4cbc-9ec1-05ea2492761b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thegeorge3?sortOrder=0&page=1'
WHERE id = '04ad0b58-9b19-4f58-9926-91873efc8969';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/the-gilmore-takeaway/0nojrM5dX6SAmj7bHmJsew'
WHERE id = '04ebb7b6-124f-48ab-9ab5-61dee7e9b872';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-hill/chill-grill'
WHERE id = '04f1440c-d14c-4fc8-b6a6-d3ad57ad2ec6';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/the-kandyan-bristol',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/the-kandyan-restaurant/j__nTyznQCyPWV2237L_Iw'
WHERE id = '05117f56-48a1-4a23-94a6-4cd1a8a29a00';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/homegrowngardencentre?sortOrder=0&page=1'
WHERE id = '05368d65-2d19-4b46-89b2-0a1c1f245f52';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = '05cf8257-67f1-48eb-b9c6-cdf5a0b7cf55';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '05e2f54f-5fbb-44ef-b1cd-065a2d42d3af';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = '05e976ca-550b-46a6-8413-08c21523124a';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/hong-kong-chef/EuDf-f2lWYqfsbOz_lgbyA'
WHERE id = '05fba952-0366-4c01-b5f6-4bd7cabbed63';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/upper-knowle-and-totterdown/subway-broadwalk-39733'
WHERE id = '0642344b-e66b-4e4b-89c5-399379f9d08f';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/redland/lunch',
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = '067934c4-f174-4207-a472-b572c4f2eb9d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bardolinopizzeriabelliniespressobarbristol'
WHERE id = '071a40e4-39db-4eac-aab3-e79363ab432e';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/redland/lunch'
WHERE id = '076816a6-8e5f-4765-b1fe-74b105e14332';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '076f251f-17d8-42bf-a733-5ffb6a78cdd5';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redland/londis-redland-fs133'
WHERE id = '0794e39b-cee4-431b-b2b4-f72fc78fc6f6';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/gloucester-road/kal-dosa',
  booking_resdiary = 'https://dishcult.com/restaurant/dosadosa'
WHERE id = '07c36905-ae21-4afd-b5a0-9a39af0ae5cb';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/hengrove-area/4183-asda-bristol-whitchurch-superstore'
WHERE id = '07ce1d1e-8c9d-4806-bfb2-8ffc11c8a2d6';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/DaGianniRestaurant'
WHERE id = '0816cc9a-1f31-478b-8dbd-a0e8beee67b6';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/triangle-grill/4BQVAkKgV0ifSgtqDpfLOA',
  booking_resdiary = 'https://dishcult.com/restaurant/baregrillsbristol'
WHERE id = '0859d716-e3fc-4073-a1f6-edbdbef61f54';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/stockwood-area/stockwood-fish-bar'
WHERE id = '089b0bd2-bb58-406e-ad47-a6735b599a80';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bristolloafatthebeacon?sortOrder=0&page=1'
WHERE id = '08b6f45c-7cab-463a-8d5e-9081c7ae7e7a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/salvatoresmedfordsquare'
WHERE id = '08e44930-c59f-4e8e-a6bc-d2f25473437d';

UPDATE public.listings SET
  booking_resdiary = 'https://www.dishcult.com/restaurant/goldencranebristol?sortOrder=0&page=1'
WHERE id = '08fcc74f-d4a8-4a96-a4ba-e70a2e8488ba';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/hotwells/rontec-hotwells'
WHERE id = '0903e8a9-24d0-4b10-9c6f-2a1d255cba77';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thehandandflowers'
WHERE id = '090553ca-d29f-48a9-b68a-b58ce200b8bb';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/marling-fish-bar/dbcZL0TiUmqiK3Vk-cEfQw'
WHERE id = '0983a63d-bf9a-4327-badd-6ab60f1f91f8';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/salamabites'
WHERE id = '0a10352f-26e1-46eb-8990-81146c47c494';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/vice?sortOrder=0&page=1'
WHERE id = '0a326b40-23ab-4fd2-8f77-c3e7aad49016';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/hengrove-area/4183-asda-bristol-whitchurch-superstore'
WHERE id = '0a5030e0-9913-482e-a450-8f5b19108807';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-marsh/popeyes-lousiana-kitchen-bristol-avonmeads'
WHERE id = '0a749e0b-fa17-4a38-bb97-5a0e19c8ad21';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashton-gate/als-tikka-grill'
WHERE id = '0ae95f53-51f4-4bb1-9f40-c441143741d1';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/joyraj'
WHERE id = '0aecdd74-b3aa-4b6b-bac5-3893e37f0dcc';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/parsons-bakery-ltd'
WHERE id = '0b324121-9ed5-4aa9-9912-d7502afe84ae';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = '0b5f4f79-1caa-4caa-9ec7-426e4165c979';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chloespianobar'
WHERE id = '0bb0e976-41fe-4be7-9751-c95928e708a8';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '0be76300-fd22-4a1e-a837-3ef38f35f9e8';

UPDATE public.listings SET
  booking_resdiary = 'https://www.dishcult.com/restaurant/chidowey?sortOrder=0&page=1'
WHERE id = '0c6439d5-dca6-4e74-a94f-6eda440d595b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/steakoftheartbristol?sortOrder=0&page=1&bookingDate=2022-05-22&covers=2&promotionId=0'
WHERE id = '0c820670-f6e4-4222-b6cc-d83aabdd193e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/hatter-house-cafe',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/hatter-house-cafe/sh-wsytnS82zr3490O4fUQ'
WHERE id = '0d128049-4853-49a1-adbe-2614de5f33d2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = '0ed04f28-3f43-4ac4-9d96-cf1c5bcb6301';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/tonight-josephine-bristol/new-bar-spy'
WHERE id = '0f0f6d1a-4f15-4bb4-921c-151f6b8a9da0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/skybluerestaurant?sortOrder=0&page=1&bookingDate=2024-06-05&covers=2&promotionId=0&bookingTime=19:30'
WHERE id = '0f5a98de-9b97-4341-983b-fdf9a7575c7f';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/anstees-bakery/U2ulLri6WL60coVC3xhHgQ'
WHERE id = '0f6166a9-5b12-48e6-bc56-223243b493b5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cave?sortOrder=0&page=1'
WHERE id = '0f75bc90-1d4e-4935-a6ed-c58bed5cb11f';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/whitchurch-area/royalty-takeaway-bs14-ah'
WHERE id = '0fdbff0d-afc1-4850-a442-82d749efdae8';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/dixy-chicken-stokes-croft/qWBriDEJX2KaDKb5oM7Zbg'
WHERE id = '1050ad8c-c0c0-403f-a77f-ad1daf83a117';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/the-ox',
  booking_resdiary = 'https://dishcult.com/restaurant/theox'
WHERE id = '10519567-9214-4c22-8881-7f2ea8e169d7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/musebrasseriebristol?sortOrder=0&amp;page=1&page=1'
WHERE id = '10758064-c5c2-4dce-b46f-452fcf32767a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/lamaya7?sortOrder=0&page=1'
WHERE id = '108d749f-a0bc-428a-8add-b308fe2352b2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/brewersinn'
WHERE id = '10ba62e8-d5e7-4d8e-bff8-a17bb26f094d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/hotwells/talwar-kitchen'
WHERE id = '10e8a871-d6d4-4b39-afd2-a5b905d62c5c';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/anna-cake-couture'
WHERE id = '10fb76ac-1bf1-4dac-bdaf-30690b99b3d8';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theblackhorse1?sortOrder=0&page=1'
WHERE id = '11a25451-483d-44a8-94b8-3205cf5d4c43';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/forestersarms'
WHERE id = '1221f727-dc31-42e5-977e-d2472f872b70';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/themagnetbar'
WHERE id = '124c0f7d-d2ed-4c26-940c-4095ce3bcedf';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/littlefrench?sortOrder=0&page=1'
WHERE id = '12cba2cc-e867-44b4-8346-3d06b7063ec5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebakehouse1'
WHERE id = '136ba848-94fe-4328-aa3e-227e2d05b159';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/morrisons-daily-bristol-hartcliffe-bishps/nwGyl_j-VSGsdGsvo5XGYA'
WHERE id = '137e9f8f-7fb6-4ece-a7c0-cd702068b332';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/matfenhallcloistersrestaurantandbar?sortOrder=0&page=1'
WHERE id = '13b5b72c-811e-4dcf-8e28-fdbd88cc5c3a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/skybluerestaurant?sortOrder=0&page=1&bookingDate=2024-06-05&covers=2&promotionId=0&bookingTime=19:30'
WHERE id = '13c7d523-e25a-42f7-8215-e97b2cff168b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bar44bristol'
WHERE id = '13e689c9-a6b6-422a-aa46-0ec377b1827d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoxfordgarden'
WHERE id = '144d7b8b-cc56-4f1f-a573-20faf574b582';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broomhill-and-brislington/wingers-brislington'
WHERE id = '1482a247-7a0b-46a0-9829-572dc7683bd3';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/prego3'
WHERE id = '14a4c5e8-34c6-4567-9685-24dcd47b653e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/eggless-cake-shop-bristol'
WHERE id = '14be5681-fe3d-4b92-8831-43ac87170f1f';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/baldwins-street-wraps/tx-DXtuORdmNJGBut4AcPA'
WHERE id = '14cea146-91a1-4f4f-bd5e-b3e0fe9a6791';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/stockwood-area/co-op-stockwood',
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = '1546a5f0-0170-44f5-9094-1fc224ddc571';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bar44bristol'
WHERE id = '15980afd-3c64-4678-9c2c-46f30caeeb56';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thefleeceatruleholme?sortOrder=0&page=1'
WHERE id = '15a77d06-af1e-44d4-8ccc-04e9a6a99d49';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/montpelier-station/take-a-break-124-cheltenham-road',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/take-a-break/wIiNg3_PWDaveQWysx8ETg'
WHERE id = '15b87dd6-0258-4765-b036-063f74a2063c';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '1696c330-ef8c-4ad3-bf6f-c0bfa9455634';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/the-bagel-place-bristol/Weq73f_DVtCDm5-hnI8RFA'
WHERE id = '16c2e893-a575-44d4-b2c1-29c185060c19';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = '16ca1819-8738-46a4-8603-4d6c2abfce2b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theredchurch'
WHERE id = '1704a61e-db5f-405e-a2d7-0eb1aab09efe';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = '172f2454-09b7-4288-aec9-66ca29763aa9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theboardroomhull?sortOrder=0&page=1'
WHERE id = '174cb019-2a3e-4243-acd9-3274a699e3ec';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/goldencranebristol'
WHERE id = '17520ff5-0e3c-4a48-97ae-6392665746e5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '1768cb6c-5ab0-4abd-bcd3-0fe22f2bf598';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-marsh/mcdonalds-0533'
WHERE id = '17cd3512-b5de-4b20-a4df-3703bf063420';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thepumphouse?sortOrder=0&page=1'
WHERE id = '17fb03be-c051-47ab-9f44-99d84c2a9a29';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '181c46e8-16ed-4ed1-ad57-3d61d313ab3d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pieministerbristolbroadquay'
WHERE id = '186ce654-4b7c-43f9-b641-1e05a8c05174';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mugshotrestaurants?sortOrder=0&page=1'
WHERE id = '18adf967-ab06-4d4c-a557-cb14482b1149';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/tikka-express'
WHERE id = '190913e6-2467-4e62-8a5f-048560235732';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/arbordiningbar'
WHERE id = '19e8b1b7-7974-421a-af26-7dbda24d6029';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/littlehollowspasta'
WHERE id = '1a3470ef-ad7b-42ef-8d3c-5666585cb063';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = '1a7c7dc6-9f94-4ae0-a091-543d9b58d0c3';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/terracecharcoalgrillloungebar?sortOrder=0&page=1'
WHERE id = '1a9eeef1-956f-4bcd-b603-33218603756a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thelazydog'
WHERE id = '1aa7f13b-67dd-48f5-9671-2597158187e4';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bardolinopizzeriabelliniespressobarbristol'
WHERE id = '1ad0231b-be9d-42f0-bbd9-e6cb9e73aff5';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/boston-tea-party-park-street'
WHERE id = '1b08dcd7-3eeb-4ce1-9ab2-9e9f1e244ac5';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/pret-a-manger-bristol-queens-road/6EjFiJhhQieCQl6UxAAHRQ'
WHERE id = '1b23a1a8-04d6-40f6-a1fa-035811fcd01d';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/white-lion/WIouFKPMVeuWmf_-67zHJQ',
  booking_resdiary = 'https://dishcult.com/restaurant/whitelionhotel1?sortOrder=0&page=1'
WHERE id = '1b6e3e5b-3346-49f1-8710-1675f0b3f9ef';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebakehouse1'
WHERE id = '1bc2179e-5e60-4cc0-91f3-ca6195b86ced';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/topcut?sortOrder=0&page=1'
WHERE id = '1c2dd3c4-d5d4-4e1f-8ea3-76c4bd28f2c9';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/shirehampton/dragon-i-bristol',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/dragon-i/V_gHju1SUzKC-uRzR9q7yQ'
WHERE id = '1c422916-3b5e-408c-b538-0c1d9d77a3de';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/lonelymouth'
WHERE id = '1c653243-160d-44c2-8390-9f563c42c113';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/shirehampton/4047-asda-shirehampton-express-petrol'
WHERE id = '1c9dca57-4e6d-4980-921e-c07e9e3fe49f';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/redland/lunch'
WHERE id = '1cbe6f25-5eba-47b9-8a47-e7ab47dff14f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/zhucanton'
WHERE id = '1cbf3fb5-c499-4ac3-8a56-a1e2536c5901';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thewindmillrestaurantskiathos'
WHERE id = '1cc1bb4c-ed5e-47e3-9100-b3fe4d145319';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '1cd1cad3-3682-4715-a29a-4537b467a4b0';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/nutmeg',
  booking_resdiary = 'https://dishcult.com/restaurant/nutmeg'
WHERE id = '1d0e878a-49bf-4806-a973-a8b61f9789bd';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/milk-bun',
  booking_resdiary = 'https://dishcult.com/restaurant/milkthistle?sortOrder=0&page=1'
WHERE id = '1d36a6db-793c-4c80-a799-7c67c78dec27';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/newmoontapascliftonvillage'
WHERE id = '1db38771-aa5a-41e2-923c-72a66c1d3d63';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thehandandflowers'
WHERE id = '1e347997-718b-4c78-a0df-26df69864174';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/dextersatbrowns'
WHERE id = '1e780d40-354b-475e-803d-c5efe799dd66';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '1e854360-495a-4f4e-88db-c85171470b87';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = '1e91a710-70fb-49f9-9690-b83044057974';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/grounded-horfield'
WHERE id = '1ea3f345-d9fc-4445-93b3-092480e45b37';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/jjohnsons'
WHERE id = '1ed07d45-0b33-4360-9e5e-de7786bb97e5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/swallowsnest1?sortOrder=0&page=1'
WHERE id = '1ee50c6b-5fe4-4270-a53b-96d46c761205';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '1f8eeb6d-76b3-4045-a72a-9db8b3d65f75';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/brentry-and-henbury/mm-kebab-pizza-henbury',
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '1f95afdf-6b6e-4b7f-95ae-ebba4f795f8a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/threebrothersburgers'
WHERE id = '203f603f-02de-41e6-ac73-2db9c7c85c8d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/lawrence-weston-and-henbury/co-op-lawrence-weston',
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = '20cab84f-2044-48c0-bab8-56885542fc59';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/smokebox'
WHERE id = '2112146c-07c6-4654-8673-068a183b6ecb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bracebrowns?sortOrder=0&page=1'
WHERE id = '21c2770a-e252-482e-a8ed-98a80e4e2483';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theparkersarms?sortOrder=0&page=1'
WHERE id = '21cf0f53-6c89-44ed-a5cd-31656a1304c5';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/thai-express-kitchen-bristol'
WHERE id = '22151dcb-55d5-493a-a59d-7455025a3064';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thegardenofeaston1'
WHERE id = '22828015-87f9-478a-924b-3e63e94c1a5e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/goldencranebristol'
WHERE id = '22be5361-d773-478b-8ca8-4235c4091c95';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thefullmooninn?sortOrder=0&page=1'
WHERE id = '22cdc9d4-627b-4464-9435-48a75ab57254';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/piazza-di-roma'
WHERE id = '240c79bd-ecd7-451a-9345-d69c60699ef5';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '24161ef9-e44e-463f-b386-032e7944812e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/henchicken'
WHERE id = '2436170c-36a5-4bed-a633-73859a4e4c54';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/gloucester-road/the-coconut-tree-gloucester-road'
WHERE id = '246bb86b-c0db-4fb2-b559-2cc02ab7cd59';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/gloucester-road/the-coconut-tree-gloucester-road'
WHERE id = '247bea9a-31a0-4b16-b84c-9ce54d806f13';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/happy-house/834BnRRTXx2slyBOPtjsBA'
WHERE id = '2493c7c5-cb87-4403-af5f-ed12d9aa5887';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = '25658c4d-a380-405a-b3e0-1a86d1deae9c';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/gloucester-road/mangosteen-gloucester-road',
  booking_resdiary = 'https://dishcult.com/restaurant/mangosteen?sortOrder=0&page=1'
WHERE id = '25837718-1ffe-491f-91d7-e678150d1770';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '258abb10-aad5-4cdd-88ca-4b87ca2630d3';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/dhamaka?sortOrder=0&page=1'
WHERE id = '25c4a218-0729-42c4-8765-c938a9420cde';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = '26975db6-0b53-49a1-973f-6985994ec3ce';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '26d9596f-71d8-4f42-97d8-8044e8da331b';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/giggling-squid-clifton',
  booking_resdiary = 'https://dishcult.com/restaurant/gigglingsquidclifton?sortOrder=0&page=1'
WHERE id = '26faec46-682b-4df7-8c69-bcf1f4ab880d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/wingstop-bristol'
WHERE id = '27661ddf-0f1b-48ad-8178-5ee108c3f0ce';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theroyaloak1'
WHERE id = '27df742f-4e31-47cc-804c-6f93d638ca65';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theshakespeare?sortOrder=0&page=1'
WHERE id = '282a3ec6-0afb-4a78-89d0-57d764716b2e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/stoke-bishop-and-sneyd-park/welcome-co-op-stoke-bishop-5-druid-hill'
WHERE id = '2889cd2f-aa39-41d8-a549-40796d6dd3c7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theorchardaccor16381'
WHERE id = '28a80c4a-c380-4799-83fa-0d857e5d5bc0';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/maxin-chicken-easton-road',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/maxin-chicken-easton/9xmAS_GtWe6t4uXmdxA2ug'
WHERE id = '291e7164-be34-41db-8718-2c013f0e4e76';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/best-kebab-old-market-43-old-market-street'
WHERE id = '2923f379-a884-4505-b962-5d5456d6006b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/lepetitlapin?sortOrder=0&page=1&bookingDate=2024-05-04&covers=2&promotionId=0&bookingTime=19:30'
WHERE id = '2925b6e2-ea1c-4f3b-93b7-d18456f1b37a';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '2937a2ae-0c47-46a2-a8a2-f3ce2876dbac';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/tgifridayscabotcircus?covers=2&amp;bookingDate=2024-02-15&amp;bookingTime=19:30&amp;sortOrder=0&amp;page=1&amp;promotionId=110897'
WHERE id = '29596f14-8dc0-4766-a9d3-5a6eaec0dc77';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/upper-knowle-and-totterdown/my-treats-knowle'
WHERE id = '29a3db62-88ef-43dc-b72a-c81feb28d91e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/holeinthewall?sortOrder=0&page=1'
WHERE id = '2a2ecc5c-32d1-498c-94cf-74122149720e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/greenroom'
WHERE id = '2a7b0044-10d2-4dd6-ae0b-40564b5206cc';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-marsh/sports-lounge-bristol-t-a-supreme-kitchen-bristol',
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = '2a908258-9974-4cf0-9c23-2f2251f0f7df';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/boigers-at-the-kingsdown-vaults-29-31-kingsdown-parade'
WHERE id = '2acdc37c-1c70-4fa5-8a17-616eef95c9dd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/hopeanchor'
WHERE id = '2b279f2d-2e79-4b10-b4d3-a05f309be114';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/zestcafebakehouse'
WHERE id = '2b2cf7b9-e6de-446a-a6cb-aaa01a1d80a0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chandosrestaurant'
WHERE id = '2c9460b6-3aac-439a-bb5f-7b1d0ea13e3e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/vanoosh'
WHERE id = '2d09cce7-9e39-4927-84c5-05a9e5c907e3';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southmead-and-henbury/smooth-fire-caribbean-flavours'
WHERE id = '2d09cf42-4ee9-4512-93cb-25f492f82145';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/st-werburghs/cafe-napolita'
WHERE id = '2d0e2542-e488-4d01-b2f1-a9e0a4790711';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/the-juke-box-bars'
WHERE id = '2d368fe2-2ba3-4cc6-be65-41b4a2c9511a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bokman'
WHERE id = '2d519a14-fba5-4002-81f9-866d7fe9e6a7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/saltpepperhonefoss'
WHERE id = '2d9fbc6e-ea8d-44f9-bf33-183ea9a49adc';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/jeans-bistro'
WHERE id = '2da45029-fab1-40d9-817f-77eaaabd610f';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/st-pauls/lunch'
WHERE id = '2e219125-bbdc-4545-b880-ede8cccbc7c7';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/m%26m-kebab-pizza-%26-fried-chicken-avonmouth/UByALe0aWUunDWVYtsJFgQ',
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '2e2e8149-f1b3-4cda-90f8-10c0655e7c4f';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol',
  booking_resdiary = 'https://dishcult.com/restaurant/theofficeeatdrinklounge'
WHERE id = '2e3550c9-5a16-410d-9528-37b13e4c84f0';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/clifton/no-4-clifton-village'
WHERE id = '2e628aa2-07a4-451f-9419-c459fef35157';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/giosbylalombarda'
WHERE id = '2e84ae2e-392f-4954-a692-1c5fef131811';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/turtlebaybristol?sortOrder=0&page=1'
WHERE id = '2f369a2c-38b9-4f1b-9ead-b329f906bede';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bardolinopizzeriabelliniespressobarbristol'
WHERE id = '2f6f3bb5-7a21-4d15-8e80-8f9a8cd835b0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/parkregishotel'
WHERE id = '2f988a96-6e95-425a-b7c2-73095698fe4a';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/clifton-thai-bristol',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast',
  booking_resdiary = 'https://dishcult.com/restaurant/cliftonthai'
WHERE id = '2fe72430-2c4b-4a0b-844c-6340fb898d1a';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/best-kebab-old-market-43-old-market-street'
WHERE id = '30140323-dd57-4f59-9fe1-2271e52e3beb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/toro'
WHERE id = '30231411-9378-4ef9-b4e1-a8e477ef8de0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = '303421ce-5c34-421c-8556-38c5ab7c89e0';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/windmill-hill-victoria-park/the-park-bakery-knwl'
WHERE id = '304b108e-72c9-449e-a97d-95ada33ffb57';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bracebrowns?sortOrder=0&page=1'
WHERE id = '3092c68c-0354-4891-9ffd-444803625743';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/therisingsun2?sortOrder=0&page=1'
WHERE id = '30ddc435-3736-4c63-b89c-d2f4e7168781';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/edencafeclifton?sortOrder=0&page=1&bookingDate=2023-06-29&covers=2&promotionId=0'
WHERE id = '312883f7-a339-48ef-b696-bcc38662b998';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thepressclub1'
WHERE id = '312d4ff1-803d-458c-8d84-e056dda6d681';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '31c0dbb3-f9c1-4959-a8e6-5020a41497f6';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/best-kebab-old-market-43-old-market-street'
WHERE id = '3208097c-362a-4674-918e-43ca559585f0';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/marcos-olive-branch/nebtT0DFUzKW69hDAkiQkw',
  booking_resdiary = 'https://www.dishcult.com/restaurant/marcosnewyorkitaliansouthgloucestershire'
WHERE id = '32824362-ba50-49cf-bd9f-a46977ca5e0b';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '32aaf395-cb86-4c77-93ad-1b5189384056';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast',
  booking_resdiary = 'https://dishcult.com/restaurant/coppaclifton'
WHERE id = '32c212a5-1e73-4edc-98b2-fcac7dddf7b7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/whitelionhotel1?sortOrder=0&page=1'
WHERE id = '32d5565d-728b-4a15-a34c-4df692b5fb83';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '33637196-9e62-4cfb-8fd5-26c7de19f16a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/oscars2'
WHERE id = '33b36a2e-ea8b-43f9-806d-c20ffd459a42';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thevintagetearoomatashwellco?sortOrder=0&page=1'
WHERE id = '33d28ddd-7be6-4134-8efb-d310d93fe420';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '344dfbaa-d4d0-4ebf-9efd-0fbea50a74f2';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southmead-and-henbury/southmead-kebab',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/southmead-kebab/hznsW-djVtSL7LS1w9HhQA'
WHERE id = '34f328b2-cfef-4d5c-94c9-3e1ae34d53f6';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chandosrestaurant'
WHERE id = '358e6230-87eb-475c-91e9-f5e898a1d16f';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/bedminster-down/the-kings-head-bristol'
WHERE id = '35afa290-db4c-43a6-b374-0a8bdee2661e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/zara-restaurant-bristol'
WHERE id = '35b5c126-c784-4ee5-a942-e13f552d7918';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/pizzarova/85V81zm0V5-RmlcSMWef0w'
WHERE id = '35bedfe5-f324-478e-b201-58cd35f776d4';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/ginjuicemumbles?sortOrder=0&page=1'
WHERE id = '36226432-ba5a-4cb3-9a7a-a9b5681c8225';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/westburyparkpub'
WHERE id = '3626e8fc-65da-4676-9ac6-cd63bc5684c4';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/discopizzapalace'
WHERE id = '36c12528-24d4-4fa8-bad5-c37ee0de468f';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '37acda09-0a6d-4ecd-85e7-a2d4e7832e6f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/sevenluckygods?sortOrder=0&page=1'
WHERE id = '3803bc47-5857-4d74-bc87-6f8caa0cd2fe';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/mcdonalds-horsefair/f6oA0X-KR6Cn8tvIYmqMSg'
WHERE id = '380a6419-2cbd-42cd-8efd-d62ed958d982';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/blame-gloria-bristol/new-bar-spy',
  booking_resdiary = 'https://dishcult.com/restaurant/londoninn?sortOrder=0&page=1'
WHERE id = '38120eb3-fc62-4ca4-bb55-5fcd85fe75ce';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thethreetunslichfield?sortOrder=0&page=1'
WHERE id = '3957b6ea-a0ee-4b2a-9ac5-731a741fe90f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pieministerbristolbroadquay'
WHERE id = '395f3239-9747-4364-810a-886ab292aed0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/therangeatbroadlands?sortOrder=0&page=1'
WHERE id = '398b7244-2706-4d43-b25b-91eb1d4a3549';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/abcrest?sortOrder=0&page=1&bookingDate=25+Jan+2022&bookingTime=19:30'
WHERE id = '399b4a28-22cc-45b2-a429-3ce34be32986';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = '3a2879cf-9354-415d-97c4-c9d150b98efc';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cave?sortOrder=0&page=1'
WHERE id = '3ac39064-2018-434d-9ca8-9ac9df07c1f9';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/zizzi-clifton'
WHERE id = '3ac905f5-8534-4909-aca5-12b33a9c20d9';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/breakfast'
WHERE id = '3b004da9-3afa-45b4-839f-9de608fb26f0';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/1st-choice-florist'
WHERE id = '3b0aedb0-4213-47c3-9c4a-25778d239a83';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '3b0d0883-5de4-4a10-a533-47e7d82c6665';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/oliveandfig'
WHERE id = '3b132bcf-9a99-44eb-8bf3-61fd94c6ce2b';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/old-market/the-old-market-assembly'
WHERE id = '3b31fc64-1db1-44ab-84c1-a3250ca0b292';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/pocha',
  booking_resdiary = 'https://dishcult.com/restaurant/horangeepocha'
WHERE id = '3b4c8e99-e99f-45ea-8a8b-da2820b43b43';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/blame-gloria-bristol'
WHERE id = '3bd62c41-49c0-4ba2-ad23-a3dcb32c6366';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/seupizzailluminati?sortOrder=0&page=1&bookingDate=2024-02-04&covers=2&promotionId=0'
WHERE id = '3c31982e-e2cc-4f05-97c6-4a37d615d1f1';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cottowinebarkitchen?sortOrder=0&page=1'
WHERE id = '3c385719-442f-4f54-a851-df75f98e5c0f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theritual?sortOrder=0&page=1'
WHERE id = '3c4d0508-d13a-415d-8880-25c5d3663279';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/shanghaioriental'
WHERE id = '3c66fdec-eb55-4aa1-b710-0a90704a7d2f';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/shanghai-garden/Fj64vGmaTHatpidrqWrgJw',
  booking_resdiary = 'https://dishcult.com/restaurant/shanghaioriental'
WHERE id = '3c887fbd-b33d-44e7-b241-3de35f92e974';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/eastville-park/10547-kfc-bristol-fishponds'
WHERE id = '3c978d6a-2e3f-4a81-b6f9-8e421dd616c1';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pizzaworkshopnorthstreet'
WHERE id = '3cd53c02-2bc2-4d42-a186-dbd34e97e4c7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thepressclub1'
WHERE id = '3e438a4f-5e29-469c-8b85-e0af88c5d8b9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pizziummilanoviasolari'
WHERE id = '3e6b0921-ed82-4a9a-8d04-d6c45bece691';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chophouseatfutureinnbristol?sortOrder=0&amp;page=1'
WHERE id = '3e87f17e-dd6d-47bb-8c6f-5ffabdd23f6c';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/las-iguanas-bristol-harbourside/ibjokgyyVXifJt3VnN9nig'
WHERE id = '3ee7d71a-060e-4886-96ae-6d10da265bbd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/criterionhotel'
WHERE id = '3fbf3b7d-2239-4310-9d6f-d59c179b2ca9';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/gourmet-kings-by-burger-king/cLaD1vMmUxW-iZwMm8UEgQ'
WHERE id = '3fcdeee5-2753-4a92-8319-7a35b1047699';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/burgertheory?sortOrder=0&page=1'
WHERE id = '3fe658c7-5a86-4fd3-babe-bf6137cf6b5a';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/redland/lunch'
WHERE id = '40517144-01ee-467e-9f2d-ba30206dbd52';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thethreelions'
WHERE id = '40d3c539-9ac8-42f9-b3d2-3d0a69608a29';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '4105fa0b-5065-4ac1-b52f-dfac1e04ddbe';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/old-market/the-old-market-assembly',
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly?sortOrder=0&page=1'
WHERE id = '4130ae8f-3330-4e0f-9adf-2187912c76a5';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southmead-and-henbury/happy-chinese-takeaway-bristol-filton'
WHERE id = '43130ec0-8eca-4602-9d2c-9b55a152b71a';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/top-1-pizza',
  booking_resdiary = 'https://dishcult.com/restaurant/federicopizzaovaledal1929milano'
WHERE id = '4379b9d7-86d0-429b-a679-3e5d87ff3e7e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecrown2'
WHERE id = '43850b2b-a5f8-42d0-bdc4-76e5a670277f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theberkeleyhotelcedricgrolet?sortOrder=0&page=1&bookingDate=2024-02-05&covers=2&promotionId=0'
WHERE id = '4419b497-a639-448d-81b4-875efffda14e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = '442f9101-6566-4844-9dca-ce1f9aa049f2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thestrawberrythief?sortOrder=0&amp;page=1&page=1'
WHERE id = '447c1082-d544-49fa-b1f3-1904cfadb195';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/the-ox'
WHERE id = '44bd6a5a-6f9e-4810-894c-f39d4c587b17';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/jojos1?sortOrder=0&page=1&bookingDate=2023-07-04&covers=2&promotionId=0&bookingTime=19:30'
WHERE id = '44f0280d-31ae-45b0-9b33-dd19054f8b80';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '45223fbb-e5b6-482f-a781-bc2b14819d61';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-hill/yummy-oriental-takeaway'
WHERE id = '458b8987-6013-468b-828c-a0d2b96d1c56';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/chilli-bellies'
WHERE id = '45b29ba9-ba59-4824-8950-14615989d13f';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redland/chandos-social',
  booking_resdiary = 'https://dishcult.com/restaurant/chandosrestaurant'
WHERE id = '45ddd499-c675-4e64-9427-dab4b521ac3a';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/best-kebab-old-market-43-old-market-street',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/old-market/the-old-market-assembly'
WHERE id = '460275eb-939a-4f4d-af58-163d745de847';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/spike-island/biblos-spike-island'
WHERE id = '4604df06-deaf-4a76-a1e1-2fb961ba74f6';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/harbourside/coyote-ugly-bristol'
WHERE id = '4674b308-9a68-48bf-a8af-55c444adf9df';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = '4704197e-1ccc-44de-875b-2cea68b22b72';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '470d0789-60fb-4749-a476-ee88159667e3';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/cha-%26-chill/2hOwVM_YUwu6z3y_zzyeoA'
WHERE id = '475ef4ca-9ecf-4203-b74d-c2c2fdb5606f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chandosrestaurant'
WHERE id = '48036f7d-09c4-4d56-b50d-0e2695aec64f';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '483336f7-f496-43cd-8161-283b7bd6d0c3';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-pauls-and-st-agnes/baba-ganoush-kitchen'
WHERE id = '483842b3-6092-4059-a578-8e2884d0781c';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/handi-grill'
WHERE id = '483daeff-2565-4d6d-a8b3-be9c31198ce6';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-quarter/ye-shakespeare',
  booking_resdiary = 'https://dishcult.com/restaurant/theshakespeare?sortOrder=0&page=1'
WHERE id = '486e0624-6ac5-452b-8bc2-55bb236473e8';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/baregrillsbristol?sortOrder=0&page=1'
WHERE id = '48a75c62-cbb8-4c11-965e-b87cfc9a7ae9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mackenziescafebarbristol'
WHERE id = '48badf40-1295-4e6a-83c8-58746e8acf8b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '49154058-2f62-4101-99fb-951aa6e4536b';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/westbury-mezze-bar-restaurant/ycFJVqxuXoeQML6_Lt07-w'
WHERE id = '495c2f88-3f8d-4330-b76c-439ae8085f33';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chandosrestaurant'
WHERE id = '4a06fea0-009a-4c02-bd9f-67d946c64a10';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/bedminster-down/co-op-bedminster-down-bristol',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/breakfast'
WHERE id = '4acc265a-1528-44f5-b421-3fef9b35a8ef';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/themillhousehotel?sortOrder=0&page=1'
WHERE id = '4b0ed977-2adc-4f64-a88b-d3edf3bb9068';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pizzaworkshopnorthstreet'
WHERE id = '4b3995c6-0e7e-4dee-8bc8-27fd562fbb90';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pizzabianchi?sortOrder=0&page=1&bookingDate=2023-05-20&covers=2&promotionId=0'
WHERE id = '4b3e154c-b392-4eed-bfe5-404784959987';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bristolloafatthebeacon'
WHERE id = '4b7046a6-646c-4111-8e65-67bfd47ad62d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/goldencranebristol'
WHERE id = '4c006836-cb16-4946-adef-e8574d22d0b0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/spirited'
WHERE id = '4c00811a-bde6-4f03-b0c7-4ca01219b579';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/clifton/no-4-clifton-village'
WHERE id = '4c2e7344-47e9-4fbb-ab6c-c7f7d585ad63';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pastaripiena?sortOrder=0&page=1'
WHERE id = '4cfe9e08-4541-484b-99c8-69084347a73d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = '4d0ce960-5ddd-4709-a0ae-5645bb780f1c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/blackbearburgerwestfieldwhitecity'
WHERE id = '4d10a5ac-5ef4-4fbb-b656-6e4322b16f07';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/berthaspizza'
WHERE id = '4d2885a2-7aa3-44a7-a24f-f6e16bdda1ed';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/marchhare'
WHERE id = '4d31401c-7587-4201-82bc-67309cb156a3';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thepipeandslippers?sortOrder=0&page=1'
WHERE id = '4d800def-514c-4015-bd50-7c712edae5d1';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/montpelier-station/olvioh'
WHERE id = '4d9ca3f8-d420-457b-b1f2-241f1770ef58';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/goldencranebristol'
WHERE id = '4dbe6086-d704-4af9-a942-70b8b803b391';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thegloucesteroldspot?sortOrder=0&page=1'
WHERE id = '4de674c1-8ac7-41fe-bc70-1c69841e0cf3';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashley-down-and-bishopston/boston-tea-part-gloucester-road'
WHERE id = '4f188be6-9732-48d9-a321-e972c8237837';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/terracecharcoalgrillloungebar?sortOrder=0&page=1'
WHERE id = '4fab220f-d39a-4ca1-997e-45ceb2ae72ff';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/hopeanchor'
WHERE id = '4fcb3ba7-a9b6-47c3-a751-dd238a527b1b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thehorsejockey1'
WHERE id = '4fe6fa15-0224-46bc-a26a-633905febd7b';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/eden-cafe-clifton',
  booking_resdiary = 'https://dishcult.com/restaurant/edencafeclifton?sortOrder=0&page=1&bookingDate=2023-06-29&covers=2&promotionId=0'
WHERE id = '4ff4decb-57e5-41de-8f72-9b9c40a33f5c';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/clifton-no-4',
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/clifton/no-4-clifton-village'
WHERE id = '50518485-ae78-490b-9a23-db387ee6c0ee';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mugshotrestaurants?sortOrder=0&page=1'
WHERE id = '5083b9fd-af58-419f-a09e-310b2c2c3826';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/junction1?sortOrder=0&page=1'
WHERE id = '508ab61a-dcce-45a5-bff7-e08363775190';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/maxin-chicken-easton/9xmAS_GtWe6t4uXmdxA2ug'
WHERE id = '50991f35-a438-4993-b012-fc6026fbaaef';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/spielburger-at-everyman-bristol'
WHERE id = '50a3f974-0462-4cd4-8485-34a7cba476da';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '50d1e267-8767-437b-83c1-6ce46a5519e0';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-quarter/basilandco'
WHERE id = '510ddf1e-cddc-4cee-8c68-60b2ffcd1fbd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebristolloafbedminster'
WHERE id = '514b4a47-4a0f-494e-a3ce-d45504129e15';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/m-m-kebab-and-pizza-filton'
WHERE id = '51545b19-ebd9-48d8-acd7-63876418c354';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bristolloafatthebeacon'
WHERE id = '5185e6a2-0665-45db-8142-48a7feb5d770';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '51cf1f04-9951-4610-8c26-dea9fa303a96';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '51d37ae3-a4ae-445d-9060-275c6d28b507';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/woolly-cactus/C3JHLuHYXcyRL7U3J992yA'
WHERE id = '52093863-9cd1-44d8-ba61-a484dbfb7d9f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/1yorkplace'
WHERE id = '522a859a-a8ee-4004-8175-20e44aaed393';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/corksoutalderleyedge'
WHERE id = '5236928a-273c-4335-b5c8-51de9eb5937d';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '52491aad-5f89-4755-ac55-5f70de998d2d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/tonysbarandgrill?sortOrder=0&page=1'
WHERE id = '5258812d-2a72-413f-8d70-3f2ccfecb01b';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/hengrove-area/4183-asda-bristol-whitchurch-superstore'
WHERE id = '52d0b7e1-edf3-4584-b089-22fe49796f5d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/indian-junction-gloucester-road',
  booking_resdiary = 'https://dishcult.com/restaurant/junction1?sortOrder=0&page=1'
WHERE id = '52e92180-2c4d-47c5-9ad3-f205a23d02d2';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/chopsticks-%E7%AD%B7%E5%AD%90/3qdcVGAGQuOo6WjkCsfgoA',
  booking_resdiary = 'https://dishcult.com/restaurant/twistedchopsticks'
WHERE id = '53100877-c8a8-440b-8537-4f5600288152';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/dominos-pizza-bristol-fishponds/Rdwk1gxaUtuPFpNs4LCfqA'
WHERE id = '53bfcb56-0dff-4b26-8c3f-9f60fdd693a1';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/santiago?sortOrder=0&page=1'
WHERE id = '53cf1837-a170-4bd2-942e-2789ac1e9020';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashton-vale-area/subway-bsw',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/subway-winterstoke-road/-WtxUjUsS-Sig544IJoDUg'
WHERE id = '53f18067-75f9-48bc-b155-bd636e08a8a9';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '5435c904-21d4-4a7f-a774-5d27ed61fbdc';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/goongnoi-thai-restaurant/NziAgCXDU7Okq92qL1-XOw'
WHERE id = '54f42322-59b0-4112-9162-7ec9534a0720';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '55275f5a-fd39-47bf-92ee-9e560071bbbf';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashton-vale-area/parsons-bakery-liberty-lane'
WHERE id = '552e38b4-0a3a-4b33-b21f-53465167290e';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/tikka-express-indian-takeaway/lQwQbZeoRwW10ABsmsQy7A'
WHERE id = '5556342a-cbba-48c1-8d92-d97d0a305296';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thehideawayatdiscovery'
WHERE id = '558aad34-ffd9-4de1-a09c-639347273d37';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/yeovalleycanteen'
WHERE id = '55bb0e4c-c19a-49b8-b732-207f5b09265b';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '55e65d5b-f1aa-4c21-8ec1-5619bf333569';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '56e93f4b-f2c9-45e7-ab04-bd917e15ad3b';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-quarter/philpotts-temple-quay'
WHERE id = '5705a176-0669-4b21-bc9d-ea8b8a952244';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/namak'
WHERE id = '579a5cdd-5244-4423-8e13-614d9abfcd29';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = '57ba263c-5ba1-4fb6-aeaa-168fa6cff775';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/greggs-bristol-u9-transom-house-vict/OWBdU_1NWP-JAR4cjtGmMg'
WHERE id = '5808d7a0-5a53-483d-ac7d-102a902588e5';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/bristol-raj'
WHERE id = '5849ca81-ffec-4dc9-b79f-c3c13fb35a80';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/filthyxiii'
WHERE id = '586608a9-4d0f-4cd6-b157-5e15f1ab06b9';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-quarter/southern-co-op-bristol-redcliffe-street'
WHERE id = '586723fd-e774-4650-b57e-1c2e94b96ddd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/steakoftheartbristol?sortOrder=0&page=1'
WHERE id = '58a3e7a1-0df4-486c-94ab-832f92e9ba95';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/abcrest?sortOrder=0&page=1&bookingDate=25+Jan+2022&bookingTime=19:30'
WHERE id = '592eb516-14fa-4af7-80c1-b88996d01ec4';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/glitch?sortOrder=0&page=1&bookingDate=2023-06-02&covers=2&promotionId=0'
WHERE id = '59477ac0-033d-4604-b27c-f8d7e1601114';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = '595089aa-53fb-41b8-a9b7-463aed848df8';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/steakoftheartbristol?sortOrder=0&page=1&bookingDate=2022-05-22&covers=2&promotionId=0'
WHERE id = '5a16b7b5-f516-41fe-82e8-1eb8a61d6abb';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '5a3ced20-33b8-41bf-a667-ce9b4222e031';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thegrainbarge'
WHERE id = '5aa57971-20ee-4f47-9b54-3e87793d392f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = '5b0bf4a8-5707-4803-9ee8-764c8938bd3f';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/coombe-dingle/neeshad-balti-house'
WHERE id = '5b0f990a-6c55-40b6-aa42-5974e120449c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theofficeeatdrinklounge'
WHERE id = '5b5b3f43-a628-4f70-82fb-de01af3531a7';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/clifton-village-fish-bar/dQrKWrQEXq2YgXu5o1IWmQ',
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/clifton/no-4-clifton-village'
WHERE id = '5b728557-a887-4a17-ad12-afd41af68657';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thegalleyrestaurant'
WHERE id = '5b7bcc5d-4712-40d0-8ec7-a096ec5385b7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/momo1?sortOrder=0&page=1'
WHERE id = '5bbd3dde-42f9-4745-ac92-31cc2328846f';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/breakfast'
WHERE id = '5bce12e3-b962-40f5-bf21-bfaade98bcac';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/the-juke-box-bars'
WHERE id = '5bd0d324-22d2-4bd8-8116-5075d420453d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/montpelier-station/bento-house'
WHERE id = '5c2b222f-502d-4906-acf2-c50a6b238ae0';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/the-ox'
WHERE id = '5c2c79e6-0701-476e-aad8-6d73aa32a00e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/golden-hill/co-op-henleaze'
WHERE id = '5caafd50-4dc4-4e8a-8399-cf33bfac3b74';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashley-down-and-bishopston/burger-bear-at-the-old-nuns-head'
WHERE id = '5cc623df-d241-429c-bd7a-e41d4f1b0214';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/la-lupe-east-street-bristol/Gtjrz53IVey5T7MwSSmvNw'
WHERE id = '5cc675be-056c-434e-bfb9-f54e2dbe6c7c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/aurorabar?sortOrder=0&page=1&bookingDate=2022-09-04&covers=2&promotionId=0'
WHERE id = '5d174183-73ef-4d13-ad7b-50a03e552c93';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/everyday-thai/7ZsNuX5dWjqLkd0_zgOP5g'
WHERE id = '5d32cee2-36c2-4706-9724-2606a46f7f31';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '5d3adbb7-9a5d-4703-b446-13ee8ffd1ee7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/goldencranebristol'
WHERE id = '5d7ed565-47d8-40e7-8dc0-ecbeb136e807';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cottowinebarkitchen?sortOrder=0&page=1'
WHERE id = '5de2a7a5-96da-4f49-a2d4-e89b4fbe57aa';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '5e4339a9-1445-4a6c-b9b4-e788b0944e7b';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/brace-%26-browns/Hptg-K9LWQ-UeUylKOYomw',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/browns',
  booking_resdiary = 'https://dishcult.com/restaurant/bracebrowns?sortOrder=0&page=1&bookingDate=2023-11-29&covers=2&promotionId=0&bookingTime=19:30'
WHERE id = '5f46edf0-0445-4f14-9996-28aa36339411';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = '5f661d3d-0b13-4efe-bf2b-74a820983555';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/terracecharcoalgrillloungebar?sortOrder=0&page=1'
WHERE id = '5f7a2f4a-4092-4a7f-831b-f1aaa2913572';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mainstlocalkitchen'
WHERE id = '5f7b0365-9944-4645-b9c2-8c77c9096de3';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/omg-bristol-bar'
WHERE id = '5fcbfd5e-6f9c-4c5a-847d-923f8f7f56bd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/themagnetbar'
WHERE id = '60126f13-51be-4329-943c-525dd8d9ea38';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thechristmassteps?sortOrder=0&amp;page=1&page=1'
WHERE id = '60800481-7941-416e-aaea-ce8defd0e5e9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebayhorsetavern?sortOrder=0&amp;page=1'
WHERE id = '6087e234-0170-4cab-bd53-e1c785011510';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/mayflower-chinese-restaurant',
  booking_resdiary = 'https://dishcult.com/restaurant/mayflower?sortOrder=0&page=1'
WHERE id = '60b5c669-9b99-4b9d-a515-96c792c8a51e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southmead-and-henbury/indian-fusion-bristol'
WHERE id = '612b83ae-f37b-436a-8f0e-29b6d2c9e9be';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cappadociarestaurantbristol?sortOrder=0&page=1'
WHERE id = '616cf867-0439-452d-97b5-64a7d1e89d98';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thalieaston'
WHERE id = '624e465b-ba70-4fd9-9dca-97904fb35fc7';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southville-east/bombil',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/bombil'
WHERE id = '6311f72f-8f36-41e3-8236-e0986afd3945';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/aromas'
WHERE id = '631af2fa-a11c-42ac-8a80-bebeec739ab8';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/hotelbristol1'
WHERE id = '63215176-8336-45eb-9a13-955206ac0fb8';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/threebrothersburgers'
WHERE id = '63492538-e50d-46a4-86ab-cc37b6f122ea';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '636dc2f1-176f-4013-92f0-991cc2429fda';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/westburyparkpub'
WHERE id = '63883c6d-6790-4af0-bd85-7616c215d55e';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '639c5cb9-f774-4d54-b1db-2c3678ff04cf';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/malik-foodstore-24-26-stapleton-road'
WHERE id = '63ac82c2-9895-401f-b763-0b9b5a7d4f30';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = '63ce2909-a116-4804-9bf8-3415eea4e191';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southville-west/coronation-curry-house',
  booking_resdiary = 'https://dishcult.com/restaurant/theroyalcurryhousenarellan'
WHERE id = '63fc57e4-2ace-43f8-a0df-91a2d2eeddf7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thekensingtonarms'
WHERE id = '6453b41c-2383-4319-9b57-2f397189321b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/luigispizza?sortOrder=0&page=1'
WHERE id = '64dc9ac4-4644-4d36-9f36-d5fcdbcfa9d9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = '650ba581-56c9-4173-8caf-605e2f45e3e9';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '6511b750-11a4-42ff-b020-3cd63601d4b5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thegloucesteroldspot?sortOrder=0&page=1'
WHERE id = '655eb359-0a40-423b-8048-d69fcdde1a15';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '655ee2fb-e83b-404e-bd20-4c5a6f2aed74';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/jacobscafebargrill'
WHERE id = '6586ebfd-55f0-4460-b51f-a73672f7e976';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-marsh/boots-6481-bristol-avon-meads-retail-park'
WHERE id = '65bb4d24-b0c4-4b94-8e23-4496acf42c61';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/butlers-broadmead',
  booking_resdiary = 'https://dishcult.com/restaurant/butlersrestaurantbar?sortOrder=0&page=1'
WHERE id = '65ce0edc-ed5c-4541-b8a6-c50494dfc93e';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/the-juke-box-bars'
WHERE id = '65f68335-ae8b-4412-9602-781a702361d5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cave?sortOrder=0&page=1'
WHERE id = '66460777-f853-496a-bc69-6c70d9c5febc';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '664bc21f-f07c-4429-91f9-085f9073a1b5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mangosteen?sortOrder=0&page=1'
WHERE id = '664ec17a-756d-447f-acdc-abc838e5e148';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/musebrasseriebristol?sortOrder=0&page=1&bookingDate=2023-09-29&covers=2&promotionId=0'
WHERE id = '6652da5a-172c-4d7e-9fb9-fdcc4c2b14bd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/oscars2'
WHERE id = '66abb360-4347-4492-933a-57ca4db49e6d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/therosecrown1?sortOrder=0&page=1&bookingDate=2023-11-30&covers=2&promotionId=0&bookingTime=19:30'
WHERE id = '66c6f897-78a4-4d42-aca8-aad48c87dc4d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashley-down-and-bishopston/mula-lounge-ltd',
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = '66d8b32a-10e5-498a-9c5a-c8101471cfc5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/kiln?sortOrder=0&page=1&bookingDate=2021-11-13&bookingTime=Invalid+date&covers=2'
WHERE id = '66de9844-a55d-4630-87af-6a673995420b';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/southmead-kebab/hznsW-djVtSL7LS1w9HhQA'
WHERE id = '6702206a-8401-45d7-9702-f6fe28eee969';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/renatos'
WHERE id = '673b8486-423b-4acb-8129-0f5b279f1e12';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/gloucester-road/chi',
  booking_resdiary = 'https://dishcult.com/restaurant/chibristol'
WHERE id = '6740db68-4c0d-4fec-9f5e-0cea3fc8485a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = '6770bbb9-27af-45ae-b193-cf9e4dfadf65';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/mangosteen-bristol',
  booking_resdiary = 'https://dishcult.com/restaurant/mangosteen?sortOrder=0&page=1'
WHERE id = '679b2449-e5d3-4828-867b-7374b0035dab';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = '67ba0038-bc1e-46df-92f5-baf85df1f806';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/tribecarestaurant'
WHERE id = '685585a3-9ae7-459f-af65-b4c68bf3b970';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '68d86b5c-7588-441f-92d9-ba50b2ba2386';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theblaiseinn'
WHERE id = '693f1085-3f73-4df7-ba43-df8677f283bd';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/iceland-food-warehouse-bristol-souths/pRNf2dIJWJafCZ0dWJRJTQ'
WHERE id = '69853bd0-c525-4e2b-8595-a940776e60ae';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/westburyparkpub'
WHERE id = '6a60d9a4-f608-4841-8209-cda680442ea9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theshakespeare?sortOrder=0&page=1'
WHERE id = '6a693005-8bca-4358-bee3-bf0383f5cd08';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = '6a7583f7-98fc-4608-8849-decfc6785c45';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southville-west/vx-bristol',
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '6ab5a286-c0fd-44b7-a7cd-db79f1353f04';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theshakespeare?sortOrder=0&page=1'
WHERE id = '6b7b4746-f61e-46cd-9e10-8eea0c5f442c';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/whitchurch-area/co-op-whitchurch'
WHERE id = '6b949c52-d220-4d9a-8111-a33406105d2e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-quarter/432-pret-a-manger-bristol-victoria-street'
WHERE id = '6be2a3d6-d536-43e8-9b47-b7395880807b';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/bravos-kitchen-at-the-crafty-cow'
WHERE id = '6c5b3633-4889-49c1-8333-092f06c9c7b8';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecliftonsausage?sortOrder=0&page=1'
WHERE id = '6d26a828-207b-4252-9a79-e6533f633dde';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '6d8067ec-7897-44ae-bc4e-620dec543c3e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/kibou-japanese-kitchen-and-bar-clifton',
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/clifton/kibou-clifton'
WHERE id = '6d8c51e4-694c-4198-923f-28ad454accac';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/terracecharcoalgrillloungebar?sortOrder=0&page=1'
WHERE id = '6dff010b-a721-4e46-bbc7-5fe6dcc49959';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southmead-and-henbury/11eleven-bs10'
WHERE id = '6e51e824-d435-4111-b971-019e1bba27ba';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashley-down-and-bishopston/tomato-and-basil'
WHERE id = '6e5ca2db-1bd8-4e4f-8b89-b3e8d24d2856';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = '6e6af7ef-419d-4999-9338-90fdf8562e69';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '6e7c81d1-0616-4a13-87c8-8c2ae216015a';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/bianchis',
  booking_resdiary = 'https://dishcult.com/restaurant/bianchisrestaurant?sortOrder=0&page=1'
WHERE id = '6ea46b1b-93eb-4b06-b0d3-8eb90bbea2eb';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/crispins-fish-and-chips-bristol/WdHXMWEDW4ucRmzic0YlMQ'
WHERE id = '6eab847b-5b2a-44de-bd0b-70d4fc804ee2';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/kongs-of-kings-street'
WHERE id = '6eb52c10-57f2-48d6-85a1-18606ffc1db0';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/city-centre/crispy-dosa-bristol'
WHERE id = '6ef5668c-36b9-4676-8b61-8c1ee470fbba';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southville-east/can-can-pizza-bristol-cancanpizza'
WHERE id = '6f0804d3-3ddc-4110-a6c8-a3b48d6e2128';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mothersruin'
WHERE id = '6f26381d-5c10-4b64-a8ce-4d84d42c7459';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '6f614b13-0683-4085-be3c-f1655067f1ba';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '70f22fd5-1d56-4183-b931-591e236547c2';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/simply-fish/MUWq5J_fSluKnX_xmkfXkg'
WHERE id = '7116571f-d7c0-419e-bede-ce5a0ba9a20b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chophouseatfutureinnbristol?sortOrder=0&amp;page=1'
WHERE id = '7134058f-b20d-406d-aeb0-cbdb12108d52';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/shirehampton/ali-mahal-9-10-the-parade-shirehampton'
WHERE id = '715088ea-9241-451e-ba0b-2dcacb4effb7';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/boots-bristol-broadmead'
WHERE id = '716ab28d-65b1-4ca4-acd5-e33e97a284d3';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/clifton-village-fish-bar'
WHERE id = '7173aabd-7e71-4687-b270-cd5bcb04e63b';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/the-viet-kitchen/bv1M54-AQf2DNMtM1ppETQ',
  booking_resdiary = 'https://dishcult.com/restaurant/thesaigonkitchen'
WHERE id = '7212496d-350a-4723-ad50-832b3cbd2dd5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = '7262b120-af5c-4b6b-90e1-b90a7573ffc6';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/city-centre/hotwells-eatery'
WHERE id = '72bb9cd0-3071-4078-893f-6aada21c1261';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/las-iguanas-bristol-harbourside/ibjokgyyVXifJt3VnN9nig'
WHERE id = '73c38e51-44e5-4753-87ba-67a51ca9135b';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/cornish-bakehouse-bristol',
  booking_resdiary = 'https://dishcult.com/restaurant/thebakehouse1'
WHERE id = '74047950-b210-44d8-9528-938d1045e5f0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/sixbynicobirmingham?sortOrder=0&page=1'
WHERE id = '741eb704-68f4-4636-80ab-ccdc7d14277f';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '74dded09-a8f7-4850-98dd-d73b7df150be';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/lawrence-weston-and-henbury/lawrence-weston-fish-bar',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/papa-johns-pizza-lawrance-weston/lZR7kq8tVZuNFQunxbO1ug'
WHERE id = '750052d7-93dd-4506-aa42-2bb376dfb071';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/kibou-japanese-kitchen-and-bar-clifton'
WHERE id = '75038eef-ae6e-4141-aa54-1565f6f1f1d9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theofficeeatdrinklounge'
WHERE id = '752ed64d-e287-422a-afdb-7e3300edf293';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebridgeinn'
WHERE id = '756e7e9e-b1bd-4366-a599-4fb4e2b660d2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theroyaloak1'
WHERE id = '758af1d1-42f9-47a9-9907-c1c7ff5be441';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chandosrestaurant'
WHERE id = '75f74b51-2f5b-417b-82d4-cebcc44e1b26';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/hotwells/indian-rassasy',
  booking_resdiary = 'https://dishcult.com/restaurant/indianrassasy'
WHERE id = '771577e6-c0fb-4f67-99c5-68ff1dae4afc';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/joeysbreakfast'
WHERE id = '777032a2-3172-4bc2-b212-20916c7f1e48';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redland/casa-mexicana'
WHERE id = '7782e506-1f16-4f0e-87b4-b4950a689edc';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/belle-de-jour-florist'
WHERE id = '780b1765-4c3d-4c0c-8ac6-ac3e7013700c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pizziummilanoviasolari'
WHERE id = '78ba4921-6764-4d70-ab4a-4ea8952b6462';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '78f4bfba-4972-4223-82f2-386d2c33e6c7';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '79115b1d-eab9-4476-b9e0-5b22a2ea7aa4';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/la-lupe-east-street-bristol/Gtjrz53IVey5T7MwSSmvNw'
WHERE id = '799256f5-5201-4e3f-98ca-903106b14961';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/taka-taka-broad-quay/2agUiVv3SFGu2NgFbjLmcA'
WHERE id = '79ac9e0c-39dc-48a8-bedb-164c3d68f90f';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-marsh/the-den-bakehouse',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/iceland-food-warehouse-avonmeads/WyAhebydUZG-oXVSPKldEw'
WHERE id = '79b9d55c-bb16-4765-bcf4-a6b66f8c2306';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/upper-knowle-and-totterdown/bath-road-convenience-store-361-bath-road'
WHERE id = '79c7dd89-4752-451d-b603-2016943b505d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/buenasado',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/buenasado'
WHERE id = '79cf13c6-217b-4a52-9003-b47a2b7b2629';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/morrisons-daily-bristol-oldbury-court/Z47heKIDSyiNH_Ud6xP4Iw'
WHERE id = '79ecd163-2f1d-4c3e-abdc-9776b465c657';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashley-down-and-bishopston/bana-dessert'
WHERE id = '7a184833-cd79-4ceb-a336-afdd0fcb79bd';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/the-crafty-egg-stokes-croft/7MRDyBEjX9-NxPSTCJpQWg'
WHERE id = '7a34c252-0563-40f9-8378-0734ff5ba502';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/no12hotelbistro?sortOrder=0&page=1'
WHERE id = '7a79fdbb-c95e-44e3-8241-f2c367fbfb16';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = '7ab933b5-8670-4288-a30c-9409b5cf1e50';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/pizza-bella/mHdp8687UMOOY-SJs9tthA'
WHERE id = '7b03ea2d-717f-4cc9-952b-f425f4246a3d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thegreenman'
WHERE id = '7b15f713-e720-47c1-bfd1-23a0c743833a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/joeysbreakfast'
WHERE id = '7b4ea4af-6221-4485-a4b8-a6b3488f67b6';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/clifton-village-fish-bar',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/clifton-village-fish-bar/dQrKWrQEXq2YgXu5o1IWmQ',
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/clifton/no-4-clifton-village',
  booking_resdiary = 'https://dishcult.com/restaurant/newmoontapascliftonvillage?sortOrder=0&amp;page=1'
WHERE id = '7b7401ba-17d8-400b-a793-4005f216fc08';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = '7bfcfc12-1110-403a-960e-4a0ce352a5cd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/westburyparkpub'
WHERE id = '7c76e85b-a423-49d9-8a43-fa3c686e3b7c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pizzaworkshopnorthstreet'
WHERE id = '7ce42593-7e3f-48fe-aa2d-3233e9ad2bb6';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/chopstix-noodle-bar-bristol-broadmead',
  booking_resdiary = 'https://dishcult.com/restaurant/twistedchopsticks'
WHERE id = '7d3b7b16-00fc-4607-9140-740c5197a062';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bank'
WHERE id = '7e03ea2d-4c8c-4873-b165-ea08579b20b0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/hydecoprohibitioncocktailbar?sortOrder=0&page=1'
WHERE id = '7e0be284-e340-4ba1-ab6c-279aa667994e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/littleshopandpantry'
WHERE id = '7e62a530-724d-4980-bc48-cff3b53f8402';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = '7e89cfce-bdaa-4b0b-b164-a69dfb9c9dd0';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/43032445-costa-coffee-whiteladies-road',
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = '7f0f3b0b-f2e3-4c23-ab4e-8286d4199278';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southmead-and-henbury/new-balti-king',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/new-balti-king/tOverpJ0SQG_v_9DMNsWtw'
WHERE id = '7f230792-1b50-4bb1-b0c2-5c54f11e5b59';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '7f3b3307-0946-46ec-be8b-2e362f43f7ea';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pizzaworkshopwhiteladiesroad?sortOrder=0&page=1'
WHERE id = '7f3bf6cc-2dbe-4161-a90c-a87cbacbe17d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/upper-knowle-and-totterdown/totterdown-canteen',
  booking_resdiary = 'https://dishcult.com/restaurant/yeovalleycanteen'
WHERE id = '7fad0d71-6c87-4ee4-8b27-bc53baee2282';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mezzeatthegreendragon'
WHERE id = '7fcff8b4-932b-4d72-bfe7-1d6cd56f289a';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/little-bagel-co-baldwin-street/8pFffFyLV86AHUB8ZM0kBA'
WHERE id = '801ffd11-8b35-4835-b88e-ffa8cbfc3746';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = '804347d6-b10a-41bc-bd4a-8ca0838cbbb3';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '8055fddf-b370-43f4-8f0d-17ef668b848f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/foxgoose'
WHERE id = '805ded43-c219-4204-8608-e76a3bc97543';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/hengrove-area/crispies-oatlands-avenue'
WHERE id = '80a8d484-a3ea-4faf-a3fa-ff588921e9a7';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '80dbb1fb-4ccf-48e4-8c3d-2377502875d7';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/co-op-bishopston-gloucester-roads/mpMRdgoRWk-vcrOOt6ysug'
WHERE id = '80f7f6a3-c7cb-4f82-98cb-56e514e69dc2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/beerdcraftbeerandpizza'
WHERE id = '8105d0eb-d375-446e-8c35-111880d27f87';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = '81423992-11d9-427e-ac39-a6233430979e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broomhill-and-brislington/profi-food-store'
WHERE id = '81b8d260-6bde-4ecf-a621-5cd66e476746';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/43032445-costa-coffee-whiteladies-road'
WHERE id = '81c662fd-ac38-4f01-8874-81c3126b44f2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thaigardengalway?sortOrder=0&page=1'
WHERE id = '81c6b83d-f577-4afd-be74-12158c768966';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/redland/lunch'
WHERE id = '8228d4c6-4fc0-4ee6-b994-41e604458640';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '82633791-413b-4f42-9460-7543eb9ba712';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/joyraj'
WHERE id = '82de7afd-7ff2-436d-89de-a31af961ddd0';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/hengrove-area/hengrove-fish-bar'
WHERE id = '83257551-dfaf-4a7f-8ee0-fb37a492b4af';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/corksoutalderleyedge'
WHERE id = '832a4b81-5abb-4373-8761-51d56acb9b39';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/bargain-booze-filton'
WHERE id = '8346d73c-8482-4a6f-abea-90987cf7dfe6';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/shirehampton/4047-asda-shirehampton-express-petrol',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/asda-express-shirehampton-express-petrol/HjFCqp88UaGTdlPCWRM3kQ'
WHERE id = '837acedd-1b73-4b98-8b06-0f40922508a7';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/barrelhouse-detroit-pizza/pkCFZcoYVQ64aF9NtvFRWw'
WHERE id = '8380a823-08d2-48f0-931d-4e4b4569fbba';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thephoenixinn'
WHERE id = '838eadfe-275a-4eb0-8210-846ca0169d63';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/12521-kfc-bristol-cabot-circus'
WHERE id = '84bdd429-06af-4749-9730-5597a278bb86';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redland/kottu-hut'
WHERE id = '84f3953e-94a8-4cb5-82a5-3234f3790100';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '8528a81d-ee2c-404a-aeff-f51668883181';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/zerodegrees'
WHERE id = '85440b3d-e5eb-43dd-a010-1ae06fba9feb';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/avonmouth/captain-cod-avongrill'
WHERE id = '8599b3f3-50e5-429e-a122-a32541031bf2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebull3?sortOrder=0&page=1'
WHERE id = '85fdab9b-cb7b-49fb-945f-d9cda2a4977a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/ripplesatchowderbay'
WHERE id = '8652af0a-83a0-4df4-a485-48e06f6de84d';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/veburger-whiteladies-rd/t2u8klviUK-LZjh_5rGNdA'
WHERE id = '865e96e6-0a4b-4818-80c3-8df125ab9e7c';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '86a0f21f-daef-48f7-9b1b-12bb962f1317';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/sea-pearl/tCZtgLWxUY2AjFd_3bJbtQ'
WHERE id = '86a904d2-fd43-4745-aedf-a21cd145b8b7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = '86dcc6d8-6087-4245-a20c-9a0546615692';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/florencejesmond'
WHERE id = '873b7f18-4ae1-43f0-85b7-b913471aa739';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bliss'
WHERE id = '873bf68a-18c9-461f-8f9d-2042b9c74175';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebushinn'
WHERE id = '875343d9-9238-4b05-a8b6-72e21fd195a9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theblackhorse1?sortOrder=0&page=1'
WHERE id = '876301e3-8bec-43f2-89d8-42c33db621bb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thewindmillrestaurantskiathos'
WHERE id = '877eda46-5eb6-407e-bdd6-de611dcce30b';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/cotham-kitchen'
WHERE id = '87b69f67-4924-44f8-8158-477960859856';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/spike-island/mokoko-coffee-and-bakery-wapping-wharf',
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = '89530584-a246-42f3-ad6a-f5f1e51dc7b8';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thekingshead5?sortOrder=0&page=1'
WHERE id = '896bdc72-78f9-46cb-bff7-ac16ce7da127';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/rock-salt-bristol',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/cotham-hill/rock-salt',
  booking_resdiary = 'https://dishcult.com/restaurant/rocksalt1?sortOrder=0&page=1'
WHERE id = '896c7feb-0b67-45f7-9ce2-58abdaac13eb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/harvest2'
WHERE id = '89a27928-3f8c-490b-94ec-b84e2e3c5108';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '89eecf44-3370-49db-b155-750df9695578';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/the-crafty-egg-stokes-croft/7MRDyBEjX9-NxPSTCJpQWg',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/stokes-croft/caribbean-croft',
  booking_resdiary = 'https://dishcult.com/restaurant/thecroft1'
WHERE id = '89f30aca-f374-4fbb-8d41-5052e6920f58';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/yafo/ejR_qAyZUoqNWdwGgI95jg',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/southville/yafo'
WHERE id = '8a1b88a6-1d8d-479d-8268-fef5ebd293ac';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/morrisons-daily-bristol-charltons/oWHCnwWNTraTFEQ83IsqAA'
WHERE id = '8a558313-6378-4165-8e56-f70123ddb2af';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/aya-sushi-bristol/Wn9SDdLtUgmmQIkcGE0s4g'
WHERE id = '8a5a279a-dc38-4278-88b7-d441f5adce39';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = '8aa41036-34d5-4e1b-9466-d6fa4f3b5b46';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/papaw-bristol'
WHERE id = '8ab81147-a054-4a17-ac26-92c1fe796f0e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pizzaworkshopnorthstreet'
WHERE id = '8b17c436-d7a0-4e7c-9344-b66f6118de7d';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/honest-burgers'
WHERE id = '8b83a0cf-eb61-434f-9a15-2333f9e82ba2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theorchardaccor16381'
WHERE id = '8b9a41e2-2a62-43cd-937a-01d8140c4dcf';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/hotwells/gails-clifton-village-29-04-24',
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/clifton/no-4-clifton-village'
WHERE id = '8c812fe1-ba13-4b2c-bb0d-1586bd6916da';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/cupp-bubble-tea-park-row/qz9sc2QGVfqK-arlS9c7uw'
WHERE id = '8ce03868-8be0-41a3-917b-8b9c43ee5151';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '8d63487a-01d5-4d09-a514-0f4c2ba02a7a';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/black-sheep-coffee-queens-road/qm6m0qtLXxOaFFrN13ZNbA'
WHERE id = '8da9a047-82b9-49e8-a18e-8fddbf7ade72';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/stokes-croft/caribbean-croft'
WHERE id = '8df59319-00a5-442e-8b0d-f0d3ceae10e7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/burntwoodcourthotelquberestaurant'
WHERE id = '8e25ec83-4ff6-47b7-ba1e-937ff676f779';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/restaurantesergio'
WHERE id = '8e74ac38-dc1f-4fdb-bd8c-f6e1da6df245';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/joyraj'
WHERE id = '8ec8c85d-0c1d-4812-95e2-fb974b840fb8';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashton-vale-area/ashton-winehouse'
WHERE id = '8ed69f13-465d-46c3-93c9-93c44b3f3c04';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/salvatoresmedfordsquare'
WHERE id = '8ed8ab34-bb67-4bc3-9f1c-cbf41a61a1dc';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/montpelier-station/thali-cafe-montpelier',
  booking_resdiary = 'https://dishcult.com/restaurant/thalimontpelier?sortOrder=0&page=1'
WHERE id = '8edabeb7-4215-4598-8ffc-bb5a8085bca7';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashley-down-and-bishopston/mula-lounge-ltd',
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = '8ef00139-c720-4fd4-a20a-9da5a9c6f76a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/homegrowngardencentre?sortOrder=0&page=1'
WHERE id = '8f9fc554-1729-4e2e-94b0-7de2b448bf34';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redland/chandos-fish-bar',
  booking_resdiary = 'https://dishcult.com/restaurant/chandosrestaurant'
WHERE id = '8fb4e3d4-69f5-4cf2-9aa9-e9b2ae4ed508';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/vegan-zall-tandoori/i1CreH_nSVmqKgh2ifVH_A'
WHERE id = '8ff7c535-37cf-4c2b-9c15-4dde0ec7e427';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/flight-club-bristol'
WHERE id = '901086a8-5059-441a-a9a2-081690c22338';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/fujiyamajapaneserestaurant'
WHERE id = '9016010c-933d-4d08-b90a-eb98e1832d06';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/therobinhoodbaslow?sortOrder=0&page=1'
WHERE id = '905ce4f5-5f69-40eb-9e93-e19ff0dc89b0';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/co-op-horfield-filton-road/iCh-sejDUfW9YuskWCuneA'
WHERE id = '90b9ab1b-fe22-4c7e-946b-18d0cb6f65bd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/replaybristol'
WHERE id = '90cc18ed-b2e6-4290-9f10-07d6bfa0f318';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/afghan-tasty-corner'
WHERE id = '910c215c-b96f-4c40-a104-efa4eb2e317e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cottowinebarkitchen?sortOrder=0&page=1'
WHERE id = '9145ec45-7214-443b-b3d9-24b957ea14cd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/lascalabistro?page=2'
WHERE id = '916e87e8-72ed-4a84-b7a6-5cad850ead6e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/whitchurch-area/co-op-whitchurch'
WHERE id = '918d72c5-2b28-41ab-873c-be5b8807a2e6';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/restaurantbotanica?sortOrder=0&page=1&bookingDate=2023-05-24&covers=2&promotionId=0'
WHERE id = '91c7a75c-e381-4df3-982a-06d220d746c2';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '920c1a4f-4b5b-4b6a-9f41-9ca17e5881c6';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/the-pancake-man/lxXJg9p0Qsu7PWs0i54LUg'
WHERE id = '921715f0-18ba-4de2-abbd-c51ce33ca1e4';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '92de9453-b6d4-4e8a-af5d-7b6c48ca4303';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pocotapasbar'
WHERE id = '92e9aee3-d969-4b9c-afd1-725738825bbb';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/bristol-raj',
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '92f6c90d-4346-416a-895d-e8431257662a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = '9310c7db-8e47-4b09-a00c-399155dde743';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = '938b8614-183c-4831-830d-ddb92bf2fb89';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '94380a9a-777f-47d8-8d28-bddcb35b53d2';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/masala-bazaar-bristol/sQy-Lg_zVLmXUkdnMHIzVA'
WHERE id = '94718ca5-270e-4cc8-8bec-f0f0e9eb89e6';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-quarter/caffe-oro'
WHERE id = '94d0ad99-3f8a-445c-a219-edfe0da1d27c';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/pill-and-easton-in-gordano/spar-pill'
WHERE id = '950fe03f-84c7-480a-8ae6-71f57e8ac532';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/joyraj'
WHERE id = '95389a74-dc7e-4657-aff8-a06be3a6d673';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/bento-boss-bristol'
WHERE id = '95c5dc4c-6cfb-4858-9792-b0d66dad5125';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pebblebeachrestaurantrooms'
WHERE id = '95dd560a-1f84-43d3-b611-72993ed0810d';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = '966b31b6-054d-434d-b434-b76729eb8f7e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashley-down-and-bishopston/devs-kerala-bristol'
WHERE id = '96d81907-f683-4e0e-ab22-1127fb35b72a';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-quarter/sandwi-on-the-go-ltd'
WHERE id = '97124459-d4ce-403e-8b50-517b125e15f5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theroyalcurryhousenarellan'
WHERE id = '975b8b7f-e1c5-44d0-95d4-7f27bf25f4f8';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '9791e385-ee76-42bc-85e7-24e40399aa22';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/almaarms1'
WHERE id = '97a9b9c8-9f36-46e1-aab5-842039a54995';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/brentry-and-henbury/star-cafe-bristol',
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/casa/new-bar-spy'
WHERE id = '97aae7f9-9cfc-4d57-a2cb-068187af0a97';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = '97dea885-16ba-40f4-b788-322df3cbf4ad';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/joesitaliankitchenatkinvineyards'
WHERE id = '98193b3a-3666-4c71-96df-e7e2a477931c';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/pizzucci/7K2I2HCNXLm4Ulj-m5O2Hg'
WHERE id = '989a568f-da91-4724-b92c-c6928fa186bc';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/brentry-and-henbury/star-cafe-bristol',
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = '98bc8ba6-d1fd-4584-acf6-c6419a010a82';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/junction1?sortOrder=0&page=1'
WHERE id = '98c8375e-9e55-487a-beaa-be2b3fba44fa';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theofficeeatdrinklounge'
WHERE id = '98ce7821-3d25-4e5e-bfcd-65ba1f635d92';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/joyraj'
WHERE id = '98ea36bb-de7a-4254-b2f3-35bd29488203';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/clifton-mini-market-bs8',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = '994c7711-97cf-4569-aee6-d35d287e14a9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/yeovalleycanteen'
WHERE id = '9969352f-7646-4378-b9d0-78725735cb29';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theportlandpizzacompanyatblackbarge'
WHERE id = '99851ed0-21da-4bba-b719-e88dfe82b0aa';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bocabarfinzelsreach'
WHERE id = '99af9982-a747-45ab-b875-7af1d209243b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/tropicanarestaurantaccor16629'
WHERE id = '9a011f39-da4b-4fb3-8c84-cb0c0ff87ed3';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = '9a6c4837-92d6-4bfb-8fc9-50bcb8e28bf6';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/itsnothotpot?sortOrder=0&page=1'
WHERE id = '9a8190fa-40ff-46a9-b997-e93606f03804';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/gong-cha-bristol-34-merchant-street'
WHERE id = '9ad5f99e-a9f8-4607-ba9f-e52c5ac24f7b';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/clifton/no-4-clifton-village',
  booking_resdiary = 'https://dishcult.com/restaurant/eastvillage'
WHERE id = '9aecbcdf-4b78-46b2-a465-82fcbc62034d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chandosrestaurant'
WHERE id = '9b27f5a7-7fb2-4624-8b4e-c228126821d0';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/eden-cafe-clifton',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast',
  booking_resdiary = 'https://dishcult.com/restaurant/edencafeclifton?sortOrder=0&page=1&bookingDate=2023-06-29&covers=2&promotionId=0'
WHERE id = '9bc32b23-8a85-46cc-b31c-d7333356ccf8';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-quarter/la-panza-bristol',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/la-panza'
WHERE id = '9bde8f53-c37b-4dbc-9053-fa3941a8ebbf';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theorchardaccor16381'
WHERE id = '9bf53947-1acd-491a-b610-02ebdc909e88';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '9c1231f0-d6eb-43dd-8ce8-d1ad36de7a6e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/therevolution?sortOrder=0&page=1'
WHERE id = '9c452dab-7b83-479a-b69c-aca8e51e913e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theprinceofwales?sortOrder=0&page=1'
WHERE id = '9cade9e8-3149-4984-a91f-5174ec1a59d3';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/harbourside/tikka-flame'
WHERE id = '9d0c4aaf-9215-47f1-b3d1-46bcf7b7dfed';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '9d41d66e-4e02-495d-aac0-af24545d3c0c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/dextersatbrowns'
WHERE id = '9d707b22-f289-4e1e-a2f5-43610bde2b27';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redland/redland-tandoori-chandos-road',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/redland/lunch'
WHERE id = '9d7df08f-c19d-4cb2-9233-b03f4ecb7e31';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/bc-diner/d6OuLS3EWyuepmejeT4qEg'
WHERE id = '9d91176c-0e85-4799-8628-b925afc48607';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/old-market/gigis-pizza'
WHERE id = '9d97c898-b5dd-4f71-81ca-fd6a397b6185';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/themetropolitan'
WHERE id = '9de4ad45-18e1-46ba-952f-12190885b16b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = '9df1e321-df53-4534-9580-e8386eea5146';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/aboe?sortOrder=0&page=1'
WHERE id = '9e274c33-c8a4-4160-8e7b-6b83f1483791';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/sainsburys-local-bristol-whiteladies-roads/0fBUZZM3W8Kdbcj855xIoA',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = '9e72868b-0fba-4471-bf0b-d4be16e40423';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/anaya'
WHERE id = '9e9e9aa2-b1b1-41ca-97e2-62c5930530fc';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/diamond-kebab-kingswood/SrSCLrbfR7SRHsJiv0mQCQ'
WHERE id = '9f436d1d-dcad-4bb1-bee7-73fad0f6a38d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/montpelier-station/asian-spicy'
WHERE id = '9f577cfe-b9ff-43d4-9940-0e15c365b9ba';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/nutmeg'
WHERE id = '9fc48a2c-8c43-4e89-87f0-bc1c32827dce';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/the-juke-box-bars'
WHERE id = '9ff5601d-a223-43c0-848c-c0bb40499658';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/browns-bristol/GyfQwlmaShmcGm1wsjWzdg',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/browns'
WHERE id = 'a0c9a4dd-9203-4ca9-9b8d-1d5ae0b40341';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = 'a1034527-7f6d-41e6-b62d-e64fcd4f2108';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chandosrestaurant'
WHERE id = 'a12e53c9-3651-4592-9541-0a9694cc9cde';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southmead-and-henbury/oriental-sunrise',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/oriental-sunrise/BexCNd0_VmmtCBV3UGsXmw'
WHERE id = 'a17e57f7-5ad6-41bc-99f3-00c16ba3ba1a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/zialuciachelsea?sortOrder=0&page=1'
WHERE id = 'a1d7c862-b03c-44a0-9a3d-134664c15ce8';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-quarter/subway-victoria-street-bristol-45525',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/subway-victoria-street/9a2lmFFbRVa2l0LqQYLJeg'
WHERE id = 'a211aa9e-1cb3-42f3-aeda-3bff235051aa';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/lifeboatinn?sortOrder=0&page=1'
WHERE id = 'a2ab9a70-3356-4b22-be13-83300412df8b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/brewersinn'
WHERE id = 'a2e83c5f-504a-4cb8-9097-0b5754a49afa';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/bishopston/the-bootlegger'
WHERE id = 'a3461784-f783-45a2-a177-a584a840f04a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theberkeleyhotelcedricgrolet?sortOrder=0&page=1&bookingDate=2024-02-05&covers=2&promotionId=0'
WHERE id = 'a396923e-9431-4f8b-97a9-060812299d89';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thegreenbank?sortOrder=0&page=1'
WHERE id = 'a3b59824-c459-4d0b-989f-ee53cef18320';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/catchattheoldfishmarket'
WHERE id = 'a3ed80cc-7126-45b7-8fdb-bcbd2f82b988';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/littleshopandpantry?sortOrder=0&page=1'
WHERE id = 'a4830134-48c2-4c57-90c6-7056f687dd10';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/co-op-bishopston-gloucester-roads/mpMRdgoRWk-vcrOOt6ysug',
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = 'a4bb1782-5187-4d5d-b2af-749ee5a5c8d5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thegallimaufry?sortOrder=0&page=1'
WHERE id = 'a542f630-f0ff-4e87-a5e8-5512a2919891';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = 'a547ce88-a246-45eb-85a5-cb8e3bf6e233';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/coachhorses?sortOrder=0&page=1'
WHERE id = 'a54d52e6-31d2-474f-9c79-ff985196d3d2';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broomhill-and-brislington/subway-bath-road-26005'
WHERE id = 'a5e6f792-9c54-4f5a-9eb8-e8ef466d2040';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/homegrowngardencentre?sortOrder=0&page=1'
WHERE id = 'a5fe7007-3e22-4ef4-8e0a-f0d93b441698';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = 'a68a9032-90b6-4a40-9ad0-446de12b4ca6';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'a6e3b297-d72d-4512-9765-c286ec667e68';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/bagelicious',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/bagelicious/IQ5ROEMzVI6NZyYpc7lQug'
WHERE id = 'a747d8e7-d524-4804-bf90-647d853bf762';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = 'a774d297-af41-4143-ad9f-31c5007c70c6';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/premier-100-high-sts/882h7OYUWfaOCdxCfwnndQ'
WHERE id = 'a78d46c3-8b73-4cf6-ad05-14fbb379f002';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/goldencranebristol'
WHERE id = 'a7c5cd41-5097-4375-861d-cc080ff5eb78';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/downingsbar'
WHERE id = 'a7fa1510-c8cb-4c3a-bb8e-9e6ad30d97fc';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/ginjuicemumbles?sortOrder=0&page=1'
WHERE id = 'a80928f4-4b2f-4699-b248-71a874305dea';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecowsowwhiteladiesroad?sortOrder=0&page=1'
WHERE id = 'a8102025-0e8f-44bb-a202-cfcc6700c580';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/raj-mahal/zlyZpXaCSH2-FdoSUYdeVw',
  booking_resdiary = 'https://dishcult.com/restaurant/joyraj'
WHERE id = 'a8220e8a-0b0a-4270-8e43-3fe7b80933a6';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/seupizzailluminati?sortOrder=0&page=1&bookingDate=2024-02-04&covers=2&promotionId=0'
WHERE id = 'a9455fb1-3da7-4f3e-af57-d0f8dc61e05c';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/gloucester-road/dosa-queen'
WHERE id = 'a9a6cf94-5d61-48c4-aaad-9a7af0024470';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/casanovagreenhills?sortOrder=0&page=1'
WHERE id = 'a9b216ef-aea1-4829-b331-4fa55b4d2833';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/beets-n-roots'
WHERE id = 'aae86688-0aaa-4769-b687-2f283a12d291';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = 'ab5db755-0df4-4957-b908-676481396171';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theconservatorybar'
WHERE id = 'abc04242-2bdd-421b-8b82-66a33be1de3d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cave?sortOrder=0&page=1'
WHERE id = 'abcd4943-7917-4adb-90bb-57fa54911704';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/stablescafeatnewmanorfarm'
WHERE id = 'abedbc5f-4448-4bc6-9feb-88ef2edb7e44';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/knowle-west-area/morrisons-daily-hengrove-way'
WHERE id = 'ac2d4985-99f2-47db-9dc3-82608cd91882';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/bambalan',
  booking_resdiary = 'https://dishcult.com/restaurant/bambalan?sortOrder=0&page=1'
WHERE id = 'ac674793-83aa-4f43-9578-a0ae24ba4a58';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thetrooper'
WHERE id = 'ac791667-a350-4c5f-ac92-b3a529c63c9b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cafe31'
WHERE id = 'addc3dae-cf36-4830-ad1c-8638eacf21d5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/jadepalace'
WHERE id = 'ae2b16b6-b734-4f4a-9a4c-a03928b8de06';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'af025f2e-eb0b-4be8-ae44-fd09401f26c7';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashton-vale-area/ashton-winehouse'
WHERE id = 'af17edeb-6b49-4822-b032-32a0ba6daed4';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/iontheharbour?sortOrder=0&page=1&bookingDate=2024-03-28&covers=2&promotionId=0&bookingTime=19:30'
WHERE id = 'af3be118-0b32-4c6d-b797-aad99c8b3b11';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/tonysbarandgrill?sortOrder=0&page=1'
WHERE id = 'af925752-10ce-4f66-b433-25096798d6dc';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mackenziescafebarbristol'
WHERE id = 'afd50ace-ee74-4159-85ad-053601f2dca1';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/alis-curry-palace/vMQhsrxRT_WKjORacS-yhw'
WHERE id = 'afe986e8-ec8e-4e40-b870-9e93b4075b26';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebellsapperton?sortOrder=0&page=1'
WHERE id = 'b01a1822-31c1-4cec-9d5a-efba01ad40eb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theritual?sortOrder=0&page=1'
WHERE id = 'b01cb0ae-3b8a-4157-9fa1-aa1337fcbcb0';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/wagamama-bristol-cabot-circus/Zebqii1xVTCANNmAzOiKag'
WHERE id = 'b08c8ea6-bfec-4b42-8848-ae0fbef862e8';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/colosseum?sortOrder=0&page=1'
WHERE id = 'b145d5c8-becb-4f4a-9cb8-9a1136c570d3';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/hatter-house-cafe/sh-wsytnS82zr3490O4fUQ'
WHERE id = 'b14ff097-f9d3-48b9-ac62-4d81b9afb8d1';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/harbourside/pizza-express-bristol-harbourside'
WHERE id = 'b1fdbafc-ead2-44ab-8821-04d58b0489c5';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/city-centre/tonkotsu'
WHERE id = 'b235a585-7191-4878-95a6-453a0da1922d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/elgrecoleeds'
WHERE id = 'b2a43be9-b253-4794-8d2d-9389984d8e8d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theprinceofwales?sortOrder=0&page=1'
WHERE id = 'b2ee1ec4-427c-489e-8001-0b0fbd6d9c7c';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/redland/lunch'
WHERE id = 'b3594998-0295-4e1f-b7ee-bb41f16fea27';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/813-caffe-nero-bristol-whiteladies-road'
WHERE id = 'b38b9589-0b90-493f-8845-fa28cd9db0c7';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/tasty-to-go-%E8%88%8C%E5%B0%96%E5%8D%A4%E5%91%B3/pwqdJNY9WEOuvVqiT8f_Ug'
WHERE id = 'b40cc6d3-2d5d-4bfe-97e2-2f06cef6a2d3';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = 'b4520c0e-aad5-41a3-b222-172479a691fe';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = 'b45cfac2-4e50-455b-993e-3d1a0fcba4fa';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/vegan-achari-kitchen'
WHERE id = 'b48f7d33-3770-49fe-80d6-b6abe0d819e7';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/bristol-raj',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/the-ox'
WHERE id = 'b51f90d6-bd52-46f5-bcb1-757150f9dee3';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/parkregishotel'
WHERE id = 'b53e28a0-4e26-4c17-a9b2-6c2593ddbce3';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/clifton/steam-bristol',
  booking_resdiary = 'https://www.dishcult.com/restaurant/goldencranebristol?sortOrder=0&page=1'
WHERE id = 'b550ec6d-e5b4-4ff4-833d-346153285bba';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/bedminster-down/chaitan-news'
WHERE id = 'b65469ba-bc46-435f-92ef-615170130af1';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/gloucester-road/dosa-queen'
WHERE id = 'b66686b1-bc91-4815-9959-66eafb84a3f1';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/sainsburys-local-bristol-whiteladies-roads/0fBUZZM3W8Kdbcj855xIoA',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = 'b67713f2-3163-44f5-9210-a2f42cbb43a1';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/bristol-raj'
WHERE id = 'b68d72f6-7dc8-4a37-adc3-bea5b15eb5a3';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = 'b6a0f1a6-4c6b-4bd1-ad44-af182a27994b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/edencafeclifton?sortOrder=0&page=1&bookingDate=2023-06-29&covers=2&promotionId=0'
WHERE id = 'b6b6be27-cd81-4414-a976-b35ad407f1b0';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = 'b6bbc15f-6a40-4a6e-98e9-8eb011c5c185';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecrown2'
WHERE id = 'b7a8100e-e7f7-4804-ba3b-e74404c899b1';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/ginjuicemumbles?sortOrder=0&page=1'
WHERE id = 'b81f38c0-6b7c-4dbb-b558-ffaf25ef6047';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/redland/lunch'
WHERE id = 'b8a28a0e-0e1d-493c-a2a9-08fae9d23b44';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-pauls-and-st-agnes/the-green-melon-bristol'
WHERE id = 'b910fb5d-e76d-491b-8a5e-deb078686719';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/upper-knowle-and-totterdown/bath-road-convenience-store-361-bath-road'
WHERE id = 'b9281263-9af6-44a7-bd12-ae8c18410170';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/olivetreeturkishrestaurantandbarbedford'
WHERE id = 'b944184c-e96d-4a22-9128-f079ce84187f';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/morrisons-daily-bristol-highridges/NkYM2gh_Vw28GzgECln--g'
WHERE id = 'ba300b31-254a-4b4a-93f1-c8a75e5fc329';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/hugosrestaurant1?sortOrder=0&page=1'
WHERE id = 'ba8571e0-f0c1-4052-a947-d976c04ce3f8';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/noa-japanese'
WHERE id = 'bad76d59-d903-4d06-81c3-227c50af78a6';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/king-street-raj',
  booking_resdiary = 'https://dishcult.com/restaurant/joyraj'
WHERE id = 'bb7ff065-7469-423b-8cf4-103e07408807';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/asia-express-bristol'
WHERE id = 'bc4ae564-d964-4777-9363-84aa9dd61410';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/the-viet-kitchen/bv1M54-AQf2DNMtM1ppETQ',
  booking_resdiary = 'https://dishcult.com/restaurant/thesaigonkitchen'
WHERE id = 'bce4f226-d190-4eed-9c61-53f12ee7be7f';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'bd1bd093-9740-41b9-b864-df88480c8137';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecottageinn'
WHERE id = 'bd1e1add-8cf9-4604-8c33-62daa07a21ef';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = 'bd8948e5-816b-44ae-b10f-850599c90ca4';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/leftbank'
WHERE id = 'bdcdd197-c735-463b-9f62-5990c82c1600';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'bdf13216-7560-419f-9f35-3b4687e68abb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thewoodstockarmsoxford'
WHERE id = 'bec2cb2e-5363-4b19-a942-03cfe59010f1';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thepackhorse?sortOrder=0&page=1'
WHERE id = 'bed2a2ab-e28e-423e-aa86-37062a516209';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/goldencranebristol'
WHERE id = 'bee2489d-070f-4eb2-9302-b2d97d487234';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/indian-kitchen/2FSPhsr1QKiJzpiGQb9tAQ',
  booking_resdiary = 'https://dishcult.com/restaurant/achariindiankitchen'
WHERE id = 'bf011ef9-5a58-40c5-a81f-0ec4cbc1c432';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebeehivemontpellier'
WHERE id = 'bf0b6a2b-aa4c-4b5e-a8df-481ef3027fe1';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thepressclub1'
WHERE id = 'bf1082c6-e6ad-4693-a74b-3ce8acc051b1';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/bar-44'
WHERE id = 'bf268307-b024-4b89-8ad6-4768d1d6ccbd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = 'bf6993f7-7494-4fe9-9da9-bb68b6db0075';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-pauls-and-st-agnes/waaberi-restaurant-and-takeaway-152-ashley-road',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/waaberi-restaurant/9BZonKcbUg6umt373Vxm0g'
WHERE id = 'bf764f54-dcaa-4f5d-a329-2a6207024b8a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/wilsons'
WHERE id = 'bfb304b2-3c59-46cd-aeb6-219db504b82e';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/harbourside/the-bristol-stable'
WHERE id = 'bfc2dc00-5278-471b-a7cb-0d1557574cd3';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/poppyscafe'
WHERE id = 'bfc9f605-9e68-4bdb-9412-7e57c94e69d2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = 'c013ab08-3378-4606-a8f0-1c2645280e78';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thewhitehorsehambrook?sortOrder=0&page=1'
WHERE id = 'c0148a79-cc7b-42d5-b151-644b8282e926';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pizzaworkshopwhiteladiesroad?sortOrder=0&page=1'
WHERE id = 'c1b7f2dd-9293-482a-a7af-3545d35ef122';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/dragonsdelicacy?sortOrder=0&page=1'
WHERE id = 'c246c8cb-2c9a-46dc-98b8-8133c1f0aef7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = 'c2491dce-abc2-4185-bccc-1ee136f339e2';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/dangun'
WHERE id = 'c24c2a82-fd0f-4b2e-a005-0532c49fa924';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/fish-n-fry/V4zCiQZqVnO2Pf9GlswTig'
WHERE id = 'c26ba50c-4855-417f-8119-8d8e0a904dd7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/luigispizza?sortOrder=0&page=1'
WHERE id = 'c2acf30c-1a2c-4c05-9b8e-829af5d232c3';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/knife-%26-fork-cafe/uHd-JKL4QcGIi0QjDqnuDQ'
WHERE id = 'c2b1df28-9c4a-4697-9340-c586464470e4';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theprinceofwales?sortOrder=0&page=1'
WHERE id = 'c372f7db-cfe5-4cb1-ac87-f5333f512c7f';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/lilith-atthe-exchange'
WHERE id = 'c41da227-1f5b-4a6f-a271-62220b516f95';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/punchbowllapworth'
WHERE id = 'c434c199-af9e-4b58-82e2-5c2bcaa65644';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/terracecharcoalgrillloungebar?sortOrder=0&page=1'
WHERE id = 'c4471a9e-1f87-44d5-baa9-605f1cb1dcfb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/nomad'
WHERE id = 'c47a8fe1-907d-456e-8e91-60a7bfda2d0c';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/hotline-kabab'
WHERE id = 'c52d904b-94cd-4f56-b321-74cea6b18fb7';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/third-eye',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/third-eye-restaurant-and-bar'
WHERE id = 'c5517b96-879c-4e4b-a750-b89106196a28';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/peggysbarrestaurant'
WHERE id = 'c5c200d4-8ff1-4997-bac7-5e7652f7f0e7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = 'c6382a63-c902-4ac9-825c-c68e201257af';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/riverstation'
WHERE id = 'c69bd18c-2d1b-4cbc-9229-5451691aea4e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/burgertheory?sortOrder=0&page=1'
WHERE id = 'c6a96ca0-c5b4-41e5-906a-63db789ee984';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redland/la-campagnuola'
WHERE id = 'c7508318-ca24-4c94-8107-18f2aa11105d';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'c754833e-e1b8-4529-ad52-b8878365beeb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thestrandbar'
WHERE id = 'c7714e66-22f5-4722-8b05-d95da821f91e';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/sandwich-sandwich-baldwin-st/nTRTKalkS6m1rvcWocu2tw'
WHERE id = 'c7b09734-7172-43a2-9ad4-5ffa7b37b0dc';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/stoke-bishop-and-sneyd-park/stoke-bishop-fish-bar'
WHERE id = 'c7ca7154-a612-44f5-8166-4725b448a5d2';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = 'c80129fd-8e8a-4130-ae65-6fb2a2536f0b';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/persian-food-station-bristol'
WHERE id = 'c809dbe7-d61f-4e5f-a547-e2139d3481c0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = 'c8991822-093d-4123-b467-c09560c9fc3b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = 'c90da443-e69e-4b87-aaff-84fe3ff0419a';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southville-west/new-kings-kebab-southville'
WHERE id = 'c9fbeebc-38a1-4c0e-ac34-d638a0071109';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/bambalan',
  booking_resdiary = 'https://dishcult.com/restaurant/bambalan?sortOrder=0&page=1'
WHERE id = 'ca7d8415-ef90-4879-aa85-aa72e0d9f66c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theanchorclub'
WHERE id = 'caa8f972-13f2-4549-9a1d-3fafd687719a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theinnonthegreen1?sortOrder=0&page=1'
WHERE id = 'cac29242-2d68-4ea8-8779-1e59ad9347e2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/beerdcraftbeerandpizza'
WHERE id = 'cb2cf417-2739-4663-be4d-15e65a9805c5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/caskclyde'
WHERE id = 'cb9324aa-292e-4862-a266-8b618f829233';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-marsh/43032995-costa-coffee-avonmeads-rp'
WHERE id = 'cc029349-1a7f-457d-a9ed-3308430652f3';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/piri-piri-corner'
WHERE id = 'cc48de71-4993-4cc7-a731-be7704d0800c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theeastfieldpub?sortOrder=0&amp;page=1&page=1'
WHERE id = 'cc5d0f39-1e1e-4157-baac-7506ac70bc7e';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/omg-bristol-bar',
  booking_resdiary = 'https://dishcult.com/restaurant/momo1?sortOrder=0&page=1'
WHERE id = 'cc78353b-0374-48d8-97df-1f8596e6adee';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'ccbdf2d6-968b-4573-b332-3b88eecececd';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theshipinn8?sortOrder=0&page=1'
WHERE id = 'cdbf57a4-9147-4722-9b88-250f08c1d807';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/fryz-by-my-treats'
WHERE id = 'ce5b159f-3595-49ba-8c10-3ee31fe1fd31';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = 'ce9abc28-2b98-4683-8beb-141df403da38';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/dominic-hot-pizza-and-kebab'
WHERE id = 'cec31e87-8644-4c0f-bc19-6698a9a3c296';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/the-bowl-shed'
WHERE id = 'cec428b3-a040-4418-b7b1-4da6017b6b8f';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/catleys'
WHERE id = 'cef39524-2995-4791-a18e-fc8dee53e07e';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/real-habesha-takeaway-easton/rE9AT1aTTsyui9_0aGH7sg'
WHERE id = 'cef89e94-04f8-456c-b879-2516555a482a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thepressclub1'
WHERE id = 'cf3f501f-664d-4f79-8742-0e7f268eac37';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theredlionandsun?sortOrder=0&page=1'
WHERE id = 'cfe43824-849e-42be-836d-c918da910b0f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/granotrondheim'
WHERE id = 'd05195b5-ee5e-4ee2-b772-41b93cb84a46';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/the-crafty-egg-fish-ponds/_3ZmeKdNVSC3-gLTGKRpjw'
WHERE id = 'd05d3a02-a972-4f0a-b39a-4c3b15cf2c4d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/shirehampton/super-kebab-and-pizza-48-high-street',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/super-kebab-and-pizza/KFiQ5xXIWuO3o806ixBLzQ'
WHERE id = 'd06a60c1-08de-4824-8656-e598fbf39a37';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/sotiris-greek-bakery/WJyezxuxW0Ku0siBbk7gzg'
WHERE id = 'd09a6242-cfa9-462f-91d9-3d046a5ddb35';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/montpelier-station/big-bite-montpelier',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/big-bite/riJhoFDTRVO8oQtg7EzgCg'
WHERE id = 'd0d819d1-d3ea-4857-a462-5eb2a530f2b2';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'd1083577-9a9c-4791-bba2-ffeae14c5b15';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/vicepizzawingshopphibsborough?sortOrder=0&page=1'
WHERE id = 'd15b695b-6d4d-40db-be98-1244ef779926';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/la-lupe-east-street-bristol/Gtjrz53IVey5T7MwSSmvNw'
WHERE id = 'd174bbbd-bf1c-4b32-9ca2-a82c4128715b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecourthousecoffeebarandresturant'
WHERE id = 'd18d5ad7-b350-46aa-b4c8-270bcca541f2';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/a-taste-of-china/vVYeAOQrVgmiiWe8JrWPVQ'
WHERE id = 'd2143b2d-d04e-4a7a-a824-035887c34e14';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton-down/piazza-di-roma',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/pizzarova/85V81zm0V5-RmlcSMWef0w'
WHERE id = 'd29172fc-1db0-4e35-88f3-dd14ca2c3408';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/subway-bristol-broadmead-41509',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/subway-union-st/SC8b7tRjScWlVxLhGdXVVQ'
WHERE id = 'd31ff3f9-f9ec-41be-9cd8-25bc086caf2e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theknowle?sortOrder=0&page=1'
WHERE id = 'd3565ae8-9676-4c2b-83f5-86fef70f9b1f';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/subway-victoria-street/9a2lmFFbRVa2l0LqQYLJeg'
WHERE id = 'd35c8814-2102-4b3e-938d-1b710e349598';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/junction1?sortOrder=0&page=1'
WHERE id = 'd38a367e-b821-46bd-9a46-3b8c98197a8a';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = 'd41ff48c-99d6-4194-8bd8-a3161385a2cc';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'd42801ce-076a-4f78-9f4e-c63ffa838cbf';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = 'd452bd6e-6ab3-4751-b9bc-4f9e7e5ce541';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecricketers1?sortOrder=0&page=1'
WHERE id = 'd4fe1e76-6798-4deb-b5ce-813fdd481601';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/kabukijapaneserestaurant'
WHERE id = 'd5b51d53-bee9-46b0-b912-78dc33d3cafa';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/simply-pizza/fE8lylrhWIiMtnzCY6s0pg'
WHERE id = 'd65defde-de4c-4e5f-b29a-5095fbad9726';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/southville-west/sonny-stores'
WHERE id = 'd67403ba-6cc4-45cd-a546-9b75e26960aa';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thelanterninn?sortOrder=0&page=1'
WHERE id = 'd6781713-2dbe-4a11-83fe-439de81168b7';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/curry-garden/b7fuoaF2TkiE6IewrQwPFQ'
WHERE id = 'd6928c57-57b4-4dcb-a601-687abff395e3';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/brewersinn'
WHERE id = 'd698243d-ae58-47e9-be3a-365174539038';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/harvest2'
WHERE id = 'd6a0f80a-034a-4a8b-a419-4153ea5e652e';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = 'd6b22597-43a3-4b3a-9cc1-6b66757362ff';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/jacobscafebargrill'
WHERE id = 'd6b44640-d21a-4f75-9fd8-c9b8b3b15222';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/monte-carlo-cafe/saQt9gxiUvaSoI9k7q5ddg'
WHERE id = 'd6c75d7a-5c27-4071-8398-eeffe86c38df';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theberkeleyhotelcedricgrolet?sortOrder=0&page=1&bookingDate=2024-02-05&covers=2&promotionId=0'
WHERE id = 'd77f3573-f9f8-492e-a90c-bd06584ff35f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theloveinn?sortOrder=0&page=1'
WHERE id = 'd81f54f2-ebcb-448b-93d2-738b225b0ad2';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'd83f87a8-00ad-4f3f-b85d-e56af5f90a05';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashley-down-and-bishopston/mula-lounge-ltd',
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = 'd8610e3b-88dd-47c2-9ce1-768c9e26de4c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = 'd8bc7d9b-687f-441c-a4a7-d9131c90d17d';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = 'd8fc945c-80c1-41f9-90ed-af28b97ea4b0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecourthousecoffeebarandresturant'
WHERE id = 'd8fe209a-bdcf-4015-b483-9bca32d54ccd';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = 'd914b044-b98d-4b70-9195-9ff0a90aa0d8';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/papa-johns-pizza-lawrance-weston/lZR7kq8tVZuNFQunxbO1ug'
WHERE id = 'd91ea8f3-6e80-4e68-8fc9-4eaa9f0881a2';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/lucky-chef-chinese-takeaway-bristol'
WHERE id = 'd94f6c9f-6bdc-43d5-a176-e9538d5a6a5b';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = 'd95a69e7-39f8-4bc6-9417-d1affaafb20d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/cote-brasserie-bristol-clifton-brs',
  booking_resdiary = 'https://dishcult.com/restaurant/musebrasseriebristol?sortOrder=0&page=1&bookingDate=2023-09-29&covers=2&promotionId=0'
WHERE id = 'd9ad8394-2c8e-4935-ad7f-719c9a63e58b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = 'da06fafe-6b04-40a5-aa3e-ee236ea42d50';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'da3fa25c-7f1c-4567-bf7e-d3273f55e95b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/joesitaliankitchenatkinvineyards'
WHERE id = 'da5b9ab3-28ed-423f-b952-53c939e42b5c';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/stokes-croft/caribbean-croft'
WHERE id = 'da5dded7-00d0-4a35-a4f4-e8e0b381cebb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cathayrendezvous'
WHERE id = 'da6ef200-314f-42ca-981f-965ed70bd7a7';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/upper-knowle-and-totterdown/bath-road-convenience-store-361-bath-road'
WHERE id = 'da92a95d-015e-4e5f-8bab-97afe380819f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/westburyparkpub'
WHERE id = 'dae5c40b-3e2b-456c-8f78-96e74f8c20e0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = 'db81284a-049d-4b55-997a-63597a0b246b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/gustorestaurantcafebar?sortOrder=0&page=1'
WHERE id = 'dbc7d0c5-78c8-4ff3-abb7-f19c37edb3bd';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/waitrose-westbury-park/avPEodE8Ut6Q5sxWPr9cUw'
WHERE id = 'dc93d8a9-ec1d-4514-b9ef-5d57ce608e6a';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/redland/pazzo',
  booking_resdiary = 'https://dishcult.com/restaurant/pazzobristol'
WHERE id = 'dd402dcc-941a-4aa4-8d6f-ddf916186325';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/dtbyhiltonmaltaombrecafebistro'
WHERE id = 'dd5c73de-c177-46b8-887d-25ae0c0e9aef';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebakehouse1'
WHERE id = 'dd5d94f4-4a7b-4d90-aa45-c52ac8e605d0';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'dd9442ea-c9f2-4be5-bb8d-0cd3a18e4145';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/saltandmalt'
WHERE id = 'de295400-1f5c-40b4-84f0-f3df7e977826';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/breakfast'
WHERE id = 'de3f1ac0-2bab-46bc-ba40-ad41ed8d1eb2';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/browns',
  booking_resdiary = 'https://dishcult.com/restaurant/bracebrowns?sortOrder=0&page=1'
WHERE id = 'de8e55af-4209-4ff5-a01d-fe1dbbbada8e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thefarside'
WHERE id = 'df03902f-92b6-48a5-9b12-63e6e70caf06';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = 'df0ac036-d895-4063-b1e3-22398159a988';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/drfoster?sortOrder=0&page=1'
WHERE id = 'df435176-c427-47b6-8341-7c42e24d1025';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thelimekilncafebar'
WHERE id = 'df6a9dca-bff4-4e43-b86e-ab65043f91df';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/corksoutalderleyedge'
WHERE id = 'dfb7cbb7-50c7-4b59-88fc-8585dede98cf';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = 'dfc7f80d-70bd-4a7e-9c08-5ee02af08c35';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cafeamorebistro'
WHERE id = 'dff0b572-e6d9-46dd-a296-d4aef780c1ee';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/almakkah-halal-butchers-92-stapleton-road'
WHERE id = 'e014addc-a5c5-46d6-894d-3ac413c149f4';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/brewhouse-and-kitchen-bristol',
  booking_resdiary = 'https://dishcult.com/restaurant/monkeybrewhouse'
WHERE id = 'e03cfe87-425f-4a0e-b82c-17ac38f509e7';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/peggysbarrestaurant'
WHERE id = 'e04a939e-a751-46df-baa4-9d82150b938f';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/stockwood-area/indian-cottage-hollway-rd'
WHERE id = 'e0843398-e07e-42b9-9716-0d7d920acb10';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/clubs/city-centre/popworld-bristol'
WHERE id = 'e128dd73-a566-4f85-a8c6-534825287b37';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theofficeeatdrinklounge'
WHERE id = 'e12d680f-9a7a-4a6f-9331-9114c55d9986';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/georgesonsorrento'
WHERE id = 'e1366570-6e81-42d5-9436-c54a20cf7c54';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/izakayajapanesebarclifton'
WHERE id = 'e159dfb8-5bd3-42f5-8789-6b150ff137eb';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/zaatar-9-cotham-hill'
WHERE id = 'e17d675c-a9b6-48c6-b1aa-7d4cc3ed279f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/soukitchensouthville?sortOrder=0&page=1&bookingDate=2022-04-20&covers=2&promotionId=0'
WHERE id = 'e202f975-8d1b-4c62-92f7-9d1bc5e8a344';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thecoffeeclub1'
WHERE id = 'e2154e5e-02a5-4885-93c2-3a60ed9044d6';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/reinakitchen?sortOrder=0&page=1&bookingDate=2021-09-27'
WHERE id = 'e25094f4-fa9e-4a30-801a-c547fbb47e20';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebeckfordarms'
WHERE id = 'e2751918-d04f-4917-8779-34147a93d58b';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-marsh/pizza-1889-avonmeads'
WHERE id = 'e2957aa5-ecc4-4430-b111-d065487a023f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/goldencranebristol'
WHERE id = 'e2d22e15-8dcc-439a-b6c1-7055cf76dcf4';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/wapping-wharf/talwar-express'
WHERE id = 'e3e91cb0-8520-42f3-8a4b-067bb936e53e';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'e4f1c792-3257-408c-a12e-cf9f70af4ccc';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theparkersarms?sortOrder=0&page=1'
WHERE id = 'e5045bf4-cf3d-44fd-aee4-16edf3544866';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/wtf%21-mind-blowing-vegan-burgers-bristol-southmead-rd/14auaJUEXUCIjzfnpJk9UQ'
WHERE id = 'e50a5624-1055-4333-93c4-cb28015f961e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/luxe-desserts-and-gelato-stapleton-road'
WHERE id = 'e50dd047-7bd9-47ba-b805-fbd188a1a7d5';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/adelinayard?sortOrder=0&page=1'
WHERE id = 'e51ac58a-14dc-460e-9349-81c2dde5d868';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bar44bristol'
WHERE id = 'e567b883-a569-457b-b5ed-805965816bf4';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/hotelbristol1'
WHERE id = 'e57f53b0-a1d6-4ac3-94d5-c7a12571d65f';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/co-op-straits-parades/lDfTVDnWX-eMDbRzgwLLMA',
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = 'e598dc38-cf8a-4a06-800c-d823a05e8db4';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/themasonsarms'
WHERE id = 'e5e5d87d-ba75-4d65-9596-0678e812bf75';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/chandosrestaurant'
WHERE id = 'e60b136f-65f0-45de-8173-52f8575b9b0b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/bardolinopizzeriabelliniespressobarbristol'
WHERE id = 'e66b9a39-389d-4e9d-aa15-8116267f27dd';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/tops-pizza-bristol'
WHERE id = 'e6b9360f-507a-4864-8a57-8085c213810c';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/raj-gate-tandoori/m1HwAQXTVw6N3qAb-28whw'
WHERE id = 'e7259e33-ec83-4a4a-95ed-0e4984f3f220';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/burger-guys-gloucester-rd'
WHERE id = 'e762f653-b263-4599-b846-45d8bd9d1326';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/wellingtongastropub?sortOrder=0&page=1'
WHERE id = 'e78f727c-feca-4717-800a-10c008d5c4ca';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/pizzarova/85V81zm0V5-RmlcSMWef0w'
WHERE id = 'e7cb502c-c0ac-4e07-9aa3-fe9a83248b00';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/pepenero-cheswick-village/OhbNC3PZVbaa2_plpCycww'
WHERE id = 'e7d96035-217b-4fe9-a4f4-c2c6fc19262f';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redland/one-stop-coldharbour'
WHERE id = 'e854f31d-1ae9-4cd8-920e-e61f941e0d20';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/smokemirrors'
WHERE id = 'e8748427-09c1-4c9e-9560-18da588557f3';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theroyaloak1'
WHERE id = 'e8967611-2c6a-4478-9e44-5bc647f396ca';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'e92799a0-864b-4e6d-a20a-1719e19704d1';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/chew-magna/the-bear-and-swan',
  booking_resdiary = 'https://dishcult.com/restaurant/thebearhotel'
WHERE id = 'e963bc09-a06c-4588-996f-3418b294b776';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = 'e96abc3b-27ce-46d2-a5b7-1e3e5ddeac32';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = 'e9c84918-ad54-4c62-a4ee-af24b5c8176e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thewindmillrestaurantskiathos'
WHERE id = 'ea65b7a0-851a-4548-8d00-f20f56123d37';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashton-gate/china-capital'
WHERE id = 'eaf56e58-8031-4ff0-8fd3-00dc0d44b819';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/oak-tree-cafe-308-gloucester-road'
WHERE id = 'eb2b8df6-3292-422f-a33b-16af878919d7';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'ec03c7a8-645c-4c22-ba0f-c9c87c67569c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/cathayrendezvous'
WHERE id = 'ec68f089-8949-4146-be4c-3bbfbb78ccb0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/casabrasilbristol?sortOrder=0&page=1'
WHERE id = 'ec95dc61-f29a-4aa4-97ef-16334a9c7d34';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thesevenstarsatmarshbaldon1?sortOrder=0&page=1'
WHERE id = 'ecc4c3a9-2938-40aa-8995-6885fa9bbaeb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/granotrondheim'
WHERE id = 'ecd61e5e-83e4-4330-a752-6f34dc69d300';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/clifton/brunel-raj',
  booking_resdiary = 'https://dishcult.com/restaurant/joyraj'
WHERE id = 'ecedfe16-c872-424e-93c0-9eef12a28604';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/upper-knowle-and-totterdown/igrill-shawarma-knowle',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/igrill-shawarma/xDFpHmtjVmed-xr8FcT9lA'
WHERE id = 'ed04f1ce-aac3-4f11-bb61-82aabc8e8cfb';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/hermajestyssecretservice'
WHERE id = 'ed1123e9-37a9-4322-acbb-547cf0b648e3';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/lawrence-weston-and-henbury/new-horizons'
WHERE id = 'ed97f40b-2366-4086-b304-b8030b4faaaa';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/st-pauls/lunch'
WHERE id = 'eda7fa52-a7ef-4c55-994d-2c9b9c6cdee9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/westburyparkpub'
WHERE id = 'edc17885-aff5-42c9-84de-4aa0adaa5c5d';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = 'edec227f-bc32-49e4-9d34-92ff8241105b';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/nativevinewinebarandbottleshop?sortOrder=0&page=1'
WHERE id = 'ee064395-e87c-456b-bb48-458bdd8248c6';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/dextersatbrowns'
WHERE id = 'ee640749-4be7-41d3-a777-cf5998b57db9';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/musebrasseriebristol?sortOrder=0&page=1&bookingDate=2023-09-29&covers=2&promotionId=0'
WHERE id = 'ee8b6c85-23a4-4016-b007-01516aee1c3c';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/havelitheyard?sortOrder=0&page=1'
WHERE id = 'eec5a9a2-7a13-4884-b81b-c6c5adba8ce7';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/city-centre/back-garden-pizzeria'
WHERE id = 'ef67a5ed-62f4-4127-9481-40696113c73b';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/marina-restaurant',
  booking_resdiary = 'https://dishcult.com/restaurant/bulrush100?page=3'
WHERE id = 'ef68b900-3025-478a-a8ff-fc152ed1169f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = 'ef8d6608-f5cb-4a5d-90bf-1e50d3746f37';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = 'ef9accb7-89a9-4702-8ff6-fab7ffc1cdb6';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/izakayajapanesebarclifton'
WHERE id = 'efac5dcb-0b43-45ca-bc52-587b984af910';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/horangeepocha'
WHERE id = 'efe9178b-9bae-4372-a5b4-a654d89a5bbe';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/southville/the-malago',
  booking_resdiary = 'https://dishcult.com/restaurant/themalago'
WHERE id = 'f036139a-96a2-4aaa-b4c1-a5845af1236f';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = 'f0bcd884-9ca4-448d-a800-13374b925bdf';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/brentry-and-henbury/henbury-fryer-henbury'
WHERE id = 'f11cf6cc-a1e4-496c-b047-505742683141';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/whitchurch-area/co-op-whitchurch'
WHERE id = 'f124c87e-c344-4827-98e2-e4cb06d8adae';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theportlandpizzacompanyatblackbarge'
WHERE id = 'f155c84a-43b4-4f5b-b744-923ee50fb8e8';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/the-ill-repute'
WHERE id = 'f17bc69b-d29f-48ca-add1-9a6f54baba19';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/twistedchopsticks'
WHERE id = 'f26c96c2-73b8-41ea-99fd-a8ec8d78622a';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/yeovalleycanteen'
WHERE id = 'f308697d-4e71-4b5e-9b94-5933e722f2c2';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/greenroom'
WHERE id = 'f34dbaf5-99c9-4b4e-a027-17427c3e22cc';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = 'f36f14f3-8732-4e61-9397-e74abc6b2ffd';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/waitrose-westbury-park/avPEodE8Ut6Q5sxWPr9cUw'
WHERE id = 'f3c72700-fa38-4e1a-87a3-80dfaf82d99e';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theashvillesteakhouse?sortOrder=0&page=1'
WHERE id = 'f4365fba-a8e5-46c0-a28d-37e0fa8b0c9c';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/city-centre/franco-manca-bristol'
WHERE id = 'f494a20b-429d-4a62-8256-5d0be7dd6e82';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/central/the-ox'
WHERE id = 'f4c96827-dbcd-4315-9cea-428f9b462c12';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/zaatar-9-cotham-hill'
WHERE id = 'f53414fb-b1f8-4a0b-b74f-34f915ea1ec9';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/pizza-corner/IxJjykiuWQGACeZ9L2Notw'
WHERE id = 'f571f73a-82d3-49f9-8474-8aec7ccfeaa4';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/filton-local-shop-66-filton-road',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/co-op-horfield-filton-road/iCh-sejDUfW9YuskWCuneA',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = 'f58a2560-78a2-49a1-886a-c66d57539676';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/cotham/black-cumin',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/cotham-hill/black-cumin',
  booking_resdiary = 'https://dishcult.com/restaurant/blackcumin'
WHERE id = 'f5bf475b-9fb8-4690-b79c-d6ddac301d52';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/skybluerestaurant?sortOrder=0&page=1&bookingDate=2024-06-05&covers=2&promotionId=0&bookingTime=19:30'
WHERE id = 'f5c739a3-42b7-4ca6-83e9-3518d44ad896';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/horfield-area/bargain-booze-filton'
WHERE id = 'f63954b1-fae1-4471-9bf3-7c299139db0c';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/st-philips-and-old-market/fi-real'
WHERE id = 'f65df085-fdaa-4b4a-96f6-b5f7ff4bcd8e';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = 'f67909a4-2bec-4241-b85d-a742813140ea';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/red-hot-goodies/-gQzIjnjUIyAg35hf4OvxQ'
WHERE id = 'f67997c6-4f21-4ddc-861c-c331296a0ea6';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/pieministerbristolbroadquay'
WHERE id = 'f687603b-812f-4e5c-8c25-f960866b0ec4';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redland/the-saigon-kitchen-25-zetland-road',
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/redland/the-saigon-kitchen',
  booking_resdiary = 'https://dishcult.com/restaurant/thesaigonkitchen'
WHERE id = 'f6c8e4fc-51d6-4995-bdde-ab5bb9c2c19f';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/gather1'
WHERE id = 'f6e7c377-ae65-437d-8b7f-2bfba6337d34';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = 'f72562d8-da57-4bc5-953a-6ff5a5b8740d';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/gloucester-road/palomar'
WHERE id = 'f7c4ccf6-e7fe-4db5-9a17-87a7dc57e6a5';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/whitchurch-area/palermo-pizzeria-bristol'
WHERE id = 'f7d9bcab-80f2-46c7-8ff3-4517d31c6a49';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = 'f82c3f10-43a8-4f00-9ee0-2c51527ef9c1';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/broadmead-and-cabot-circus/229-the-perfume-shop-bristol-2'
WHERE id = 'f86a82db-31a1-44af-b68d-154214274623';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/underthestars?sortOrder=0&page=1'
WHERE id = 'f8bd89e1-b41b-4ede-993b-8b8c2f9c995e';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/ashton-gate/kfc-bristol-winterstoke-road'
WHERE id = 'f92540a9-57bf-47b5-8b3d-7e33edd42690';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/goldencranebristol'
WHERE id = 'f97161d3-875c-4348-8324-43a127bdb0fa';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/joesitaliankitchenatkinvineyards'
WHERE id = 'fa15b514-0911-49c1-bddc-36b1cbee08c6';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/recesshiltongardeninnglasgow?sortOrder=0&page=1'
WHERE id = 'fac10268-8f51-41e1-bf62-8dbb78eb9acf';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/theoldmarketassembly'
WHERE id = 'fadac3e8-b6db-4595-8a74-d18166181362';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mintmustardpenarth?sortOrder=0&page=1&bookingDate=2023-03-11&covers=2&promotionId=0'
WHERE id = 'fae773da-a51e-4bea-9a72-396e015a2fcd';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/avonmouth/parsons-avonmouth',
  delivery_ubereats = 'https://www.ubereats.com/gb/store/parsons-bakery-avonmouth/xZmSATiXQu-bQS_WtTkklg'
WHERE id = 'fb2cbd46-b084-4395-960a-a3b4bef477e0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/coachhorses?sortOrder=0&page=1'
WHERE id = 'fb51a245-2ab9-4110-89bc-db5d6cbbd637';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thelockup'
WHERE id = 'fb7983d5-8e66-4dad-9d6b-300b54f99550';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/terracecharcoalgrillloungebar?sortOrder=0&page=1'
WHERE id = 'fb79da9c-d292-4db8-87da-f8aa9eea20e0';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/suyaun-bistro/EuBk4nIBVFqPY7xh06vNhA'
WHERE id = 'fba7e6d0-e13b-4f4c-9a71-43fbccd03514';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/eightfolddimsumcocktaillounge'
WHERE id = 'fc11d2d5-a839-4bd5-834c-39f5e0fc524a';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/monte-carlo-cafe/saQt9gxiUvaSoI9k7q5ddg'
WHERE id = 'fc4ba310-9c49-4f51-a59e-b2a2095d592d';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/redcliffe-hill/the-cock-and-tail'
WHERE id = 'fc571db5-1635-4b68-a63e-267d5e603c21';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/thebaffledking?sortOrder=0&page=1&bookingDate=2023-11-13&covers=2&promotionId=0'
WHERE id = 'fc9b73ec-5ca4-4fc3-bd2c-27465cf599e1';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/restaurants/city-centre/gbk-bristol'
WHERE id = 'fd00302c-3686-4953-9916-7a44821d13b0';

UPDATE public.listings SET
  booking_resdiary = 'https://dishcult.com/restaurant/mokka'
WHERE id = 'fd568bc2-408b-4017-b324-762124a22a7d';

UPDATE public.listings SET
  booking_designmynight = 'https://www.designmynight.com/bristol/bars/city-centre/tonight-josephine-bristol/new-bar-spy'
WHERE id = 'fd876443-a8ec-4720-ab25-3a5f3a13ff20';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/clifton/breakfast'
WHERE id = 'fe52f616-d173-4558-8694-8c838d9b708c';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/bedminster/north-street-standard'
WHERE id = 'fec1efe3-3d43-456c-b633-3b38fb47ccb6';

UPDATE public.listings SET
  delivery_ubereats = 'https://www.ubereats.com/gb/store/morales-cafe-bristol/duMOZdqGXeSLFE2qJJgEjA'
WHERE id = 'fed32a1a-ffd2-41b9-9e3a-ebc1fc49e087';

UPDATE public.listings SET
  booking_firsttable = 'https://www.firsttable.co.uk/bristol/stokes-croft/nadu'
WHERE id = 'ff20022d-2386-463c-a47a-0743a28905ac';

UPDATE public.listings SET
  delivery_deliveroo = 'https://deliveroo.co.uk/menu/bristol/shirehampton/blue-dolphin-fish-8-high-street',
  booking_resdiary = 'https://dishcult.com/restaurant/thebluepelican'
WHERE id = 'ffc1ba1d-f989-44b9-9d33-050de20199a2';

ALTER TABLE public.listings ENABLE TRIGGER trg_listings_audit;

-- 959 rows updated