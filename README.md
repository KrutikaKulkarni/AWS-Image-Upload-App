# AWS-Image-Upload-App

The Application provides a picture viewing and album creating service and UI.
 All users are required to identify themselves (“login”) but not authenticate
 (no passwords, etc.)
 After identify themselves, a web page interface is presented to allow them to
 either view pictures, as well as a “title” (up to 68 characters), time and date
 created (or last modified), and a “likes” score, from 0 to 5 stars, for each picture.
 The web page will display (in large characters) the user’s identity welcome,
 such as “Picture Viewing For Steve” followed by a series of photos, each followed
 (or next to the picture) a title, created time and date, and likes score, as well
 as a method for the viewer to “vote” likes for any photo (any option for voting:
 box, slider, buttons, etc.)
 The initial web interface will also allow a user to “create” content: upload
 photos (no larger than 1 MB), and give a title for each.
 The album information is stored in a relational database (SQL), but
 the individual photos may be stored in any method desired. 
