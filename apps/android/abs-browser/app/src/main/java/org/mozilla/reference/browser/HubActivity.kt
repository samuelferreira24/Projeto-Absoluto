package org.projetoabsoluto.abs.browser

import android.content.Intent
import android.graphics.Color
import android.graphics.drawable.GradientDrawable
import android.net.Uri
import android.os.Bundle
import android.util.TypedValue
import android.view.Gravity
import android.widget.GridLayout
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.card.MaterialCardView

class HubActivity : AppCompatActivity() {

    private enum class Action {
        BROWSER,
        WEB_APP,
        SETTINGS,
    }

    /**
     * Hub is intentionally data-driven: add another HubItem here to extend a category
     * without changing the screen layout. The first App Web entry is the old Sistema
     * web app; it remains a separate project and is only opened as a browser channel.
     */
    private data class HubItem(
        val category: String,
        val title: String,
        val subtitle: String,
        val badge: String,
        val accent: String,
        val action: Action,
    )

    private val items = listOf(
        HubItem(
            category = "APLICATIVOS",
            title = "App Web",
            subtitle = "Sistema Absoluto · primeiro app web",
            badge = "WEB 01",
            accent = "#20E0D0",
            action = Action.WEB_APP,
        ),
        HubItem(
            category = "APLICATIVOS",
            title = "Navegador",
            subtitle = "Navegação completa na web",
            badge = "NATIVO",
            accent = "#35A7FF",
            action = Action.BROWSER,
        ),
        HubItem(
            category = "CONTROLE",
            title = "Configurações",
            subtitle = "Preferências e controles do ABS",
            badge = "SISTEMA",
            accent = "#A96BFF",
            action = Action.SETTINGS,
        ),
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = Color.rgb(5, 9, 16)
        window.navigationBarColor = Color.rgb(5, 9, 16)
        setContentView(R.layout.activity_hub)
        buildHub()
    }

    private fun buildHub() {
        val content = findViewById<LinearLayout>(R.id.hub_content)
        content.removeAllViews()

        items.groupBy { it.category }.forEach { (category, categoryItems) ->
            addSection(content, category, categoryItems)
        }

        addFooter(content)
    }

    private fun addSection(
        parent: LinearLayout,
        title: String,
        sectionItems: List<HubItem>,
    ) {
        val heading = TextView(this).apply {
            text = title
            setTextColor(Color.parseColor("#66D9FF"))
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 13f)
            setTypeface(typeface, android.graphics.Typeface.BOLD)
            letterSpacing = 0.12f
            setPadding(dp(4), dp(22), dp(4), dp(10))
        }
        parent.addView(heading)

        val grid = GridLayout(this).apply {
            columnCount = 2
            rowCount = (sectionItems.size + 1) / 2
            alignmentMode = GridLayout.ALIGN_BOUNDS
            useDefaultMargins = false
        }
        parent.addView(
            grid,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT,
            ),
        )

        sectionItems.forEachIndexed { index, item ->
            val column = index % 2
            val row = index / 2
            val params = GridLayout.LayoutParams(
                GridLayout.spec(row),
                GridLayout.spec(column, 1f),
            ).apply {
                width = 0
                height = dp(164)
                setMargins(dp(5), dp(5), dp(5), dp(5))
            }
            grid.addView(createCard(item), params)
        }
    }

    private fun createCard(item: HubItem): MaterialCardView {
        val accent = Color.parseColor(item.accent)
        val card = MaterialCardView(this).apply {
            radius = dp(20).toFloat()
            cardElevation = dp(3).toFloat()
            setCardBackgroundColor(Color.parseColor("#0C1421"))
            strokeColor = Color.argb(
                180,
                Color.red(accent),
                Color.green(accent),
                Color.blue(accent),
            )
            strokeWidth = dp(1)
            isClickable = true
            isFocusable = true
            rippleColor = android.content.res.ColorStateList.valueOf(
                Color.argb(45, 255, 255, 255),
            )
            contentDescription = "${item.title}. ${item.subtitle}"
            setOnClickListener { perform(item.action) }
        }

        val body = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(16), dp(15), dp(14), dp(12))
        }

        val top = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }

        val badge = TextView(this).apply {
            text = item.badge
            setTextColor(accent)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 9f)
            setTypeface(typeface, android.graphics.Typeface.BOLD)
            gravity = Gravity.CENTER
            setPadding(dp(8), dp(5), dp(8), dp(5))
            background = roundedBackground(
                Color.argb(
                    35,
                    Color.red(accent),
                    Color.green(accent),
                    Color.blue(accent),
                ),
                dp(8),
            )
        }
        top.addView(
            badge,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                dp(28),
            ),
        )

        val arrow = TextView(this).apply {
            text = "→"
            setTextColor(accent)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 22f)
            gravity = Gravity.CENTER
        }
        top.addView(
            arrow,
            LinearLayout.LayoutParams(dp(32), dp(32)).apply {
                gravity = Gravity.END
            },
        )
        body.addView(top)

        val titleView = TextView(this).apply {
            text = item.title
            setTextColor(Color.WHITE)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 18f)
            setTypeface(typeface, android.graphics.Typeface.BOLD)
            setPadding(0, dp(13), 0, 0)
        }
        body.addView(titleView)

        val subtitle = TextView(this).apply {
            text = item.subtitle
            setTextColor(Color.parseColor("#A9B7C9"))
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 12f)
            maxLines = 3
            setPadding(0, dp(5), 0, 0)
        }
        body.addView(subtitle)

        card.addView(body)
        return card
    }

    private fun addFooter(parent: LinearLayout) {
        val footer = MaterialCardView(this).apply {
            radius = dp(22).toFloat()
            setCardBackgroundColor(Color.parseColor("#0A111D"))
            strokeColor = Color.parseColor("#17304B")
            strokeWidth = dp(1)
            cardElevation = 0f
        }
        val body = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(18), dp(18), dp(18))
        }
        val title = TextView(this).apply {
            text = getString(R.string.hub_footer_title)
            setTextColor(Color.WHITE)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 16f)
            setTypeface(typeface, android.graphics.Typeface.BOLD)
        }
        val subtitle = TextView(this).apply {
            text = getString(R.string.hub_footer_subtitle)
            setTextColor(Color.parseColor("#91A4BA"))
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 12f)
            setPadding(0, dp(5), 0, 0)
        }
        body.addView(title)
        body.addView(subtitle)
        footer.addView(body)
        parent.addView(
            footer,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT,
            ).apply {
                setMargins(dp(5), dp(20), dp(5), dp(20))
            },
        )
    }

    private fun perform(action: Action) {
        when (action) {
            Action.BROWSER -> startActivity(Intent(this, BrowserActivity::class.java))
            Action.WEB_APP -> openWebApp()
            Action.SETTINGS -> startActivity(Intent(this, settings.SettingsActivity::class.java))
        }
    }

    private fun openWebApp() {
        val url = getString(R.string.abs_web_app_url).trim()
        if (url.isEmpty()) {
            Toast.makeText(
                this,
                getString(R.string.abs_web_app_url_missing),
                Toast.LENGTH_LONG,
            ).show()
            return
        }

        val intent = Intent(this, IntentReceiverActivity::class.java).apply {
            action = Intent.ACTION_VIEW
            data = Uri.parse(url)
            putExtra(BrowserActivity.EXTRA_ABS_APP_WEB, true)
        }
        startActivity(intent)
    }

    private fun roundedBackground(color: Int, radius: Int): GradientDrawable =
        GradientDrawable().apply {
            setColor(color)
            cornerRadius = radius.toFloat()
        }

    private fun dp(value: Int): Int =
        TypedValue.applyDimension(
            TypedValue.COMPLEX_UNIT_DIP,
            value.toFloat(),
            resources.displayMetrics,
        ).toInt()
}
