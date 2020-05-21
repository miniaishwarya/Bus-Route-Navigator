package com.example.challenge;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ClipData;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.appcompat.app.AppCompatActivity;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Iterator;
import java.util.Set;


public class MainActivity extends AppCompatActivity {

    /*-- CUSTOMIZE --*/

    private static String webview_url = "https://d5cc01a5.ngrok.io";    // web address or local file location you want to open in webview

    private static String file_type = "image/*";    // file types to be allowed for upload

    private boolean multiple_files = true;         // allowing multiple file upload



    /*-- MAIN VARIABLES --*/

    WebView webView;


    private static final String TAG = MainActivity.class.getSimpleName();


    private String cam_file_data = null;        // for storing camera file information

    private ValueCallback<Uri> file_data;       // data/header received after file selection

    private ValueCallback<Uri[]> file_path;     // received file(s) temp. location


    private final static int file_req_code = 1;


    @Override

    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {

        super.onActivityResult(requestCode, resultCode, intent);

        if (Build.VERSION.SDK_INT >= 21) {

            Uri[] results = null;



            /*-- if file request cancelled; exited camera. we need to send null value to make future attempts workable --*/

            if (resultCode == Activity.RESULT_CANCELED) {

                if (requestCode == file_req_code) {

                    file_path.onReceiveValue(null);

                    return;

                }

            }



            /*-- continue if response is positive --*/

            if (resultCode == Activity.RESULT_OK) {

                if (requestCode == file_req_code) {

                    if (null == file_path) {

                        return;

                    }


                    ClipData clipData;

                    String stringData;

                    try {

                        clipData = intent.getClipData();

                        stringData = intent.getDataString();

                    } catch (Exception e) {

                        clipData = null;

                        stringData = null;

                    }


                    if (clipData == null && stringData == null && cam_file_data != null) {

                        results = new Uri[]{Uri.parse(cam_file_data)};

                    } else {

                        if (clipData != null) { // checking if multiple files selected or not

                            final int numSelectedFiles = clipData.getItemCount();

                            results = new Uri[numSelectedFiles];

                            for (int i = 0; i < clipData.getItemCount(); i++) {

                                results[i] = clipData.getItemAt(i).getUri();

                            }

                        } else {

                            results = new Uri[]{Uri.parse(stringData)};

                        }

                    }

                }

            }

            file_path.onReceiveValue(results);

            file_path = null;

        } else {

            if (requestCode == file_req_code) {

                if (null == file_data) return;

                Uri result = intent == null || resultCode != RESULT_OK ? null : intent.getData();

                file_data.onReceiveValue(result);

                file_data = null;

            }

        }

    }


    @SuppressLint({"SetJavaScriptEnabled", "WrongViewCast"})

    @Override

    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);


        webView = (WebView) findViewById(R.id.webView);

        assert webView != null;

        WebSettings webSettings = webView.getSettings();

        webSettings.setJavaScriptEnabled(true);

        webSettings.setAllowFileAccess(true);


        if (Build.VERSION.SDK_INT >= 21) {

            webSettings.setMixedContentMode(0);

            webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);

        } else if (Build.VERSION.SDK_INT >= 19) {

            webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);

        } else {

            webView.setLayerType(View.LAYER_TYPE_SOFTWARE, null);

        }

        webView.setWebViewClient(new Callback());

        webView.loadUrl(webview_url);

        webView.setWebChromeClient(new WebChromeClient() {



            /*--

            openFileChooser is not a public Android API and has never been part of the SDK.

            handling input[type="file"] requests for android API 16+; I've removed support below API 21 as it was failing to work along with latest APIs.

            --*/

        /*    public void openFileChooser(ValueCallback<Uri> uploadMsg, String acceptType, String capture) {

                file_data = uploadMsg;

                Intent i = new Intent(Intent.ACTION_GET_CONTENT);

                i.addCategory(Intent.CATEGORY_OPENABLE);

                i.setType(file_type);

                if (multiple_files) {

                    i.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);

                }

                startActivityForResult(Intent.createChooser(i, "File Chooser"), file_req_code);

            }

        */

            /*-- handling input[type="file"] requests for android API 21+ --*/

            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {


                if (file_permission() && Build.VERSION.SDK_INT >= 21) {

                    file_path = filePathCallback;

                    Intent takePictureIntent = null;

                    Intent takeVideoIntent = null;


                    boolean includeVideo = false;

                    boolean includePhoto = false;



                    /*-- checking the accept parameter to determine which intent(s) to include --*/

                    paramCheck:

                    for (String acceptTypes : fileChooserParams.getAcceptTypes()) {

                        String[] splitTypes = acceptTypes.split(", ?+"); // although it's an array, it still seems to be the whole value; split it out into chunks so that we can detect multiple values

                        for (String acceptType : splitTypes) {

                            switch (acceptType) {

                                case "*/*":

                                    includePhoto = true;

                                    includeVideo = true;

                                    break paramCheck;

                                case "image/*":

                                    includePhoto = true;

                                    break;

                                case "video/*":

                                    includeVideo = true;

                                    break;

                            }

                        }

                    }


                    if (fileChooserParams.getAcceptTypes().length == 0) {   //no `accept` parameter was specified, allow both photo and video

                        includePhoto = true;

                        includeVideo = true;

                    }


                    if (includePhoto) {

                        takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

                        if (takePictureIntent.resolveActivity(MainActivity.this.getPackageManager()) != null) {

                            File photoFile = null;

                            try {

                                photoFile = create_image();

                                takePictureIntent.putExtra("PhotoPath", cam_file_data);

                            } catch (IOException ex) {

                                Log.e(TAG, "Image file creation failed", ex);

                            }

                            if (photoFile != null) {

                                cam_file_data = "file:" + photoFile.getAbsolutePath();

                                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(photoFile));

                            } else {

                                cam_file_data = null;

                                takePictureIntent = null;

                            }

                        }

                    }


                    if (includeVideo) {

                        takeVideoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);

                        if (takeVideoIntent.resolveActivity(MainActivity.this.getPackageManager()) != null) {

                            File videoFile = null;

                            try {

                                videoFile = create_video();

                            } catch (IOException ex) {

                                Log.e(TAG, "Video file creation failed", ex);

                            }

                            if (videoFile != null) {

                                cam_file_data = "file:" + videoFile.getAbsolutePath();

                                takeVideoIntent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(videoFile));

                            } else {

                                cam_file_data = null;

                                takeVideoIntent = null;

                            }

                        }

                    }


                    Intent contentSelectionIntent = new Intent(Intent.ACTION_GET_CONTENT);

                    contentSelectionIntent.addCategory(Intent.CATEGORY_OPENABLE);

                    contentSelectionIntent.setType(file_type);

                    if (multiple_files) {

                        contentSelectionIntent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);

                    }


                    Intent[] intentArray;

                    if (takePictureIntent != null && takeVideoIntent != null) {

                        intentArray = new Intent[]{takePictureIntent, takeVideoIntent};

                    } else if (takePictureIntent != null) {

                        intentArray = new Intent[]{takePictureIntent};

                    } else if (takeVideoIntent != null) {

                        intentArray = new Intent[]{takeVideoIntent};

                    } else {

                        intentArray = new Intent[0];

                    }


                    Intent chooserIntent = new Intent(Intent.ACTION_CHOOSER);

                    chooserIntent.putExtra(Intent.EXTRA_INTENT, contentSelectionIntent);

                    chooserIntent.putExtra(Intent.EXTRA_TITLE, "File chooser");

                    chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, intentArray);

                    startActivityForResult(chooserIntent, file_req_code);

                    return true;

                } else {

                    return false;

                }

            }

        });

    }



    /*-- callback reporting if error occurs --*/

    public class Callback extends WebViewClient {

        public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {

            Toast.makeText(getApplicationContext(), "Failed loading app!", Toast.LENGTH_SHORT).show();

        }

    }



    /*-- checking and asking for required file permissions --*/

    public boolean file_permission() {

        if (Build.VERSION.SDK_INT >= 23 && (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED || ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED)) {

            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.CAMERA}, 1);

            return false;

        } else {

            return true;

        }

    }



    /*-- creating new image file here --*/

    private File create_image() throws IOException {

        @SuppressLint("SimpleDateFormat") String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());

        String imageFileName = "img_" + timeStamp + "_";

        File storageDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);

        return File.createTempFile(imageFileName, ".jpg", storageDir);

    }



    /*-- creating new video file here --*/

    private File create_video() throws IOException {

        @SuppressLint("SimpleDateFormat")

        String file_name = new SimpleDateFormat("yyyy_mm_ss").format(new Date());

        String new_name = "file_" + file_name + "_";

        File sd_directory = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);

        return File.createTempFile(new_name, ".3gp", sd_directory);

    }



    /*-- back/down key handling --*/

    @Override

    public boolean onKeyDown(int keyCode, @NonNull KeyEvent event) {

        if (event.getAction() == KeyEvent.ACTION_DOWN) {

            if (keyCode == KeyEvent.KEYCODE_BACK) {

                if (webView.canGoBack()) {

                    webView.goBack();

                } else {

                    finish();

                }

                return true;

            }

        }

        return super.onKeyDown(keyCode, event);

    }


    @Override

    public void onConfigurationChanged(Configuration newConfig) {

        super.onConfigurationChanged(newConfig);

    }
}

/*
public class MainActivity extends AppCompatActivity {
    private WebView mywebview;
    //edited here
    final Activity activity = this;
    public Uri imageUri;
    private static final int FILECHOOSER_RESULTCODE=1; // back to 2888
    private ValueCallback<Uri> mUploadMessage;
    private Uri mCapturedImageURI = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Get webview
        mywebview = (WebView) findViewById(R.id.webView);

        // Define url that will open in webview. CHANGE IT
        String webViewUrl = "https://6426c57e.ngrok.io";

        // Javascript enabled on webview
        mywebview.getSettings().setJavaScriptEnabled(true);

        // Other webview options
        mywebview.getSettings().setLoadWithOverviewMode(true);

        //Other webview settings
        mywebview.setScrollBarStyle(WebView.SCROLLBARS_OUTSIDE_OVERLAY);
        mywebview.setScrollbarFadingEnabled(false);
        mywebview.getSettings().setBuiltInZoomControls(true);
        mywebview.getSettings().setPluginState(PluginState.ON);
        mywebview.getSettings().setAllowFileAccess(true);
        mywebview.getSettings().setSupportZoom(true);
        mywebview.getSettings().setDomStorageEnabled(true);

        //Load url in webview
        mywebview.loadUrl(webViewUrl);

        // Define Webview manage classes
        startWebView();


    }
*/
/*
    private void startWebView() {



        // Create new webview Client to show progress dialog
        // Called When opening a url or click on link
        // You can create external class extends with WebViewClient
        // Taking WebViewClient as inner class

        mywebview.setWebViewClient(new WebViewClient() {
            ProgressDialog progressDialog;

            //If you will not use this method url links are open in new brower not in webview
            public boolean shouldOverrideUrlLoading(WebView view, String url) {

                // Check if Url contains ExternalLinks string in url
                // then open url in new browser
                // else all webview links will open in webview browser
                if(url.contains("google")){

                    // Could be cleverer and use a regex
                    //Open links in new browser
                    view.getContext().startActivity(
                            new Intent(Intent.ACTION_VIEW, Uri.parse(url)));

                    // Here we can open new activity

                    return true;

                } else {

                    // Stay within this webview and load url
                    view.loadUrl(url);
                    return true;
                }
            }

            //Show loader on url load
            public void onLoadResource (WebView view, String url) {

                // if url contains string androidexample
                // Then show progress  Dialog
                if (progressDialog == null && url.contains("ngrok")
                ) {

                    // in standard case YourActivity.this
                    progressDialog = new ProgressDialog(MainActivity.this);
                    progressDialog.setMessage("Loading...");
                    progressDialog.show();
                }
            }

            // Called when all page resources loaded
            public void onPageFinished(WebView view, String url) {

                try{
                    // Close progressDialog
                    if (progressDialog.isShowing()) {
                        progressDialog.dismiss();
                        progressDialog = null;
                    }
                }catch(Exception exception){
                    exception.printStackTrace();
                }
            }

        });


        // You can create external class extends with WebChromeClient
        // Taking WebViewClient as inner class
        // we will define openFileChooser for select file from camera or sdcard

        mywebview.setWebChromeClient(new WebChromeClient() {

            // openFileChooser for Android 3.0+
            public void openFileChooser(ValueCallback<Uri> uploadMsg, String acceptType){

                // Update message
                mUploadMessage = uploadMsg;

                try{

                    // Create AndroidExampleFolder at sdcard

                    File imageStorageDir = new File(
                            Environment.getExternalStoragePublicDirectory(
                                    Environment.DIRECTORY_PICTURES)
                            , "AndroidExampleFolder");

                    if (!imageStorageDir.exists()) {
                        // Create AndroidExampleFolder at sdcard
                        imageStorageDir.mkdirs();
                    }

                    // Create camera captured image file path and name
                    File file = new File(
                            imageStorageDir + File.separator + "IMG_"
                                    + String.valueOf(System.currentTimeMillis())
                                    + ".jpg");

                    mCapturedImageURI = Uri.fromFile(file);

                    // Camera capture image intent
                    final Intent captureIntent = new Intent(
                            android.provider.MediaStore.ACTION_IMAGE_CAPTURE);

                    captureIntent.putExtra(MediaStore.EXTRA_OUTPUT, mCapturedImageURI);

                    Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                    i.addCategory(Intent.CATEGORY_OPENABLE);
                    i.setType("image/*");

                    // Create file chooser intent
                    Intent chooserIntent = Intent.createChooser(i, "Image Chooser");

                    // Set camera intent to file chooser
                    chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS
                            , new Parcelable[] { captureIntent });

                    // On select image call onActivityResult method of activity
                    startActivityForResult(chooserIntent, FILECHOOSER_RESULTCODE);

                }
                catch(Exception e){
                    Toast.makeText(getBaseContext(), "Exception:"+e,
                            Toast.LENGTH_LONG).show();
                }

            }

            // openFileChooser for Android < 3.0
            public void openFileChooser(ValueCallback<Uri> uploadMsg){
                openFileChooser(uploadMsg, "");
            }

            //openFileChooser for other Android versions
            public void openFileChooser(ValueCallback<Uri> uploadMsg,
                                        String acceptType,
                                        String capture) {

                openFileChooser(uploadMsg, acceptType);
            }



            // The webPage has 2 filechoosers and will send a
            // console message informing what action to perform,
            // taking a photo or updating the file

            public boolean onConsoleMessage(ConsoleMessage cm) {

                onConsoleMessage(cm.message(), cm.lineNumber(), cm.sourceId());
                return true;
            }

            public void onConsoleMessage(String message, int lineNumber, String sourceID) {
                //Log.d("androidruntime", "Show console messages, Used for debugging: " + message);

            }
        });   // End setWebChromeClient

    }

    // Return here when file selected from camera or from SDcard
    @Override
    protected void onActivityResult(int requestCode, int resultCode,
                                    Intent intent) {

        super.onActivityResult(requestCode, resultCode, intent);
        if (requestCode == FILECHOOSER_RESULTCODE) {

            if (null == this.mUploadMessage) {
                return;

            }

            Uri result = null;

            try {
                if (resultCode != RESULT_OK) {

                    result = null;

                } else {

                    // retrieve from the private variable if the intent is null
                    result = intent == null ? mCapturedImageURI : intent.getData();
                }
            } catch (Exception e) {
                Toast.makeText(getApplicationContext(), "activity :" + e,
                        Toast.LENGTH_LONG).show();
            }

            mUploadMessage.onReceiveValue(result);
            mUploadMessage = null;

        }

    }

    @Override
    public void onBackPressed(){
        if(mywebview.canGoBack()) {
            mywebview.goBack();
        } else
        {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu){
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item){
        int id = item.getItemId();

        if(id == R.id.action_settings){
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

}
*/


