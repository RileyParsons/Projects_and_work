package com.example.collection_manager


import androidx.appcompat.app.AppCompatDelegate
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.test.core.app.ApplicationProvider
import androidx.test.espresso.Espresso.onData
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.Espresso.openActionBarOverflowOrOptionsMenu
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.doesNotExist
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.contrib.RecyclerViewActions
import androidx.test.espresso.intent.Intents.intended
import androidx.test.espresso.intent.matcher.IntentMatchers.hasComponent
import androidx.test.espresso.intent.rule.IntentsRule
import androidx.test.espresso.matcher.ViewMatchers.hasDescendant
import androidx.test.espresso.matcher.ViewMatchers.isChecked
import androidx.test.espresso.matcher.ViewMatchers.isDisplayed
import androidx.test.espresso.matcher.ViewMatchers.withId
import androidx.test.espresso.matcher.ViewMatchers.withSpinnerText
import androidx.test.espresso.matcher.ViewMatchers.withText
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import com.example.collection_manager.data.db.AppDatabase
import org.hamcrest.CoreMatchers.containsString
import org.hamcrest.CoreMatchers.endsWith
import org.hamcrest.CoreMatchers.instanceOf
import org.hamcrest.CoreMatchers.`is`
import org.hamcrest.Matchers.allOf
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith


/**
 * Instrumented test, which will execute on an Android device.
 *
 * See [testing documentation](http://d.android.com/tools/testing).
 */
@RunWith(AndroidJUnit4::class)
class EspressoTests {
    @get:Rule

    val intentsRule = IntentsRule()

    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    @Test
    fun useAppContext() {
        // Context of the app under test.
        val appContext = InstrumentationRegistry.getInstrumentation().targetContext
        assertEquals("com.example.collection_manager", appContext.packageName)
    }

    @Test
    fun testButtonAdd(){
        onView(withId(R.id.AddNewItem)).perform(click())
        // se if intent activity is launched
        intended(hasComponent(Form::class.java.name))
    }

    @Test
    fun testRecyclerViewItem(){
        onView(withId(R.id.rvItemsList)).perform(click())
        // se if intent activity is launched
        intended(hasComponent(ViewItem::class.java.name))
    }

    @Test
    fun testRecyclerDeleteMessage(){
        onView(withId(R.id.rvItemsList)).perform(longClick())
        onView(withText("Delete Item")).check(matches(isDisplayed()))
    }
    @Test
    fun testSwitch(){
        onView(withId(R.id.toggle_mode)).perform(click())
        onView(withId(R.id.toggle_mode)).check(matches(isChecked()))
        // test if the current default night mode is set to yes
        assertEquals(AppCompatDelegate.MODE_NIGHT_YES, AppCompatDelegate.getDefaultNightMode())
    }

    @Test
    fun testSortOptionSelection() {
        // get size of data
        val context = ApplicationProvider.getApplicationContext<android.content.Context>()
        val db = AppDatabase.getDatabase(context)
        val dao = db.collectionDao()
        val listSize = dao.getSize()
        val lastPosition = listSize - 1

        openActionBarOverflowOrOptionsMenu(context)
        onView(withText(R.string.sort_name_a_z)).perform(click())
        // open last item and then check if expected value exists
        onView(withId(R.id.rvItemsList)).perform(RecyclerViewActions.actionOnItemAtPosition<ItemAdaptor.ViewHolder>(lastPosition, click()))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("Panzer"))))
        onView(withId(R.id.back)).perform(click())

        openActionBarOverflowOrOptionsMenu(context)
        onView(withText(R.string.sort_name_z_a)).perform(click())
        onView(withId(R.id.rvItemsList)).perform(RecyclerViewActions.actionOnItemAtPosition<ItemAdaptor.ViewHolder>(lastPosition, click()))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("Vickers"))))
        onView(withId(R.id.back)).perform(click())


        openActionBarOverflowOrOptionsMenu(context)
        onView(withText(R.string.sort_era_ww1)).perform(click())
        onView(withId(R.id.rvItemsList)).perform(RecyclerViewActions.actionOnItemAtPosition<ItemAdaptor.ViewHolder>(lastPosition -2, click()))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("Panzer"))))
        onView(withId(R.id.back)).perform(click())

        openActionBarOverflowOrOptionsMenu(context)
        onView(withText(R.string.sort_era_ww2)).perform(click())
        onView(withId(R.id.rvItemsList)).perform(RecyclerViewActions.actionOnItemAtPosition<ItemAdaptor.ViewHolder>(lastPosition -2, click()))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("Mark"))))
        onView(withId(R.id.back)).perform(click())

    }

    @Test
    fun fullCRUD(){
        // error here to address settings app in phone --> select abut phone --> press build 7 times -->
        // developer options on the bottom --> go to drawing -->
        // switch all options to animaiton off window save, transaiotn, animator
        onView(withId(R.id.AddNewItem)).perform(click())
        // see if intent activity is launched
        intended(hasComponent(Form::class.java.name))
        onView(withId(R.id.item_name)).perform(scrollTo(), click(), replaceText("Sherman"), closeSoftKeyboard())
        onView(withId(R.id.category)).perform(scrollTo(), click())
        onData(allOf(`is`(instanceOf(String::class.java)))).atPosition(2).perform(click())
        onView(withId(R.id.era)).perform(scrollTo(), click())
        onData(allOf(`is`(instanceOf(String::class.java)))).atPosition(2).perform(click())
        onView(withId(R.id.year_purchased)).perform(scrollTo(), click(), replaceText("1944"), closeSoftKeyboard())
        onView(withId(R.id.price_purchased)).perform(scrollTo(), click(), replaceText("55000"), closeSoftKeyboard())
        onView(withId(R.id.provenance)).perform(scrollTo(), click(), replaceText("American Manufacturer"), closeSoftKeyboard())
        onView(withId(R.id.description)).perform(scrollTo(), click(), replaceText("Big Tank"), closeSoftKeyboard())

        onView(withId(R.id.save)).perform(click())
        onView(withId(R.id.rvItemsList)).perform(RecyclerViewActions.actionOnItem<ItemAdaptor.ViewHolder>(hasDescendant(withText("Sherman")), click()))

        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("Sherman"))))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("WW2"))))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("Other"))))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("1944"))))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("55000"))))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("Big Tank"))))

        onView(withId(R.id.edit)).perform(click())

        onView(withId(R.id.item_name)).check(matches(withText(containsString("Sherman"))))
        onView(withId(R.id.year_purchased)).check(matches(withText(containsString("1944"))))
        onView(withId(R.id.price_purchased)).check(matches(withText(containsString("55000"))))
        onView(withId(R.id.provenance)).check(matches(withText(containsString("American Manufacturer"))))
        onView(withId(R.id.description)).check(matches(withText(containsString("Big Tank"))))
        onView(withId(R.id.category)).check(matches(withSpinnerText("Other")))
        onView(withId(R.id.era)).check(matches(withSpinnerText("WW2")))

        onView(withId(R.id.item_name)).perform(scrollTo(), click(), replaceText("M4A1 Sherman"), closeSoftKeyboard())

        onView(withId(R.id.save)).perform(click())

        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("M4A1 Sherman"))))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("WW2"))))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("Other"))))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("1944"))))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("55000"))))
        onView(withId(R.id.itemDetails)).check(matches(withText(containsString("Big Tank"))))

        onView(withId(R.id.back)).perform(click())

        onView(withId(R.id.rvItemsList)).perform(RecyclerViewActions.actionOnItem<ItemAdaptor.ViewHolder>(hasDescendant(withText("M4A1 Sherman")), longClick()))
        onView(withText("Delete Item")).check(matches(isDisplayed()))
        onView(withId(android.R.id.button2)).perform(click());


        onView(withId(R.id.rvItemsList)).perform(RecyclerViewActions.actionOnItem<ItemAdaptor.ViewHolder>(hasDescendant(withText("M4A1 Sherman")), longClick()))
        onView(withText("Delete Item")).check(matches(isDisplayed()))
        onView(withId(android.R.id.button1)).perform(click())

        onView(withText("M4A1 Sherman")).check(doesNotExist())
        // assert that name does not exist
    }

}