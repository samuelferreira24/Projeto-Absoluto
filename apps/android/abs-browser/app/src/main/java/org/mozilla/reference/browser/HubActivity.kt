package org.projetoabsoluto.abs.browser

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class HubActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hub)

        findViewById<android.view.View>(R.id.hub_browser).setOnClickListener {
            startActivity(Intent(this, BrowserActivity::class.java))
        }

        findViewById<android.view.View>(R.id.hub_web_app).setOnClickListener {
            startActivity(Intent(this, BrowserActivity::class.java))
        }

        findViewById<android.view.View>(R.id.hub_tools).setOnClickListener { }
        findViewById<android.view.View>(R.id.hub_settings).setOnClickListener {
            startActivity(Intent(this, settings.SettingsActivity::class.java))
        }
    }
}
