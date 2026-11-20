#include <wx/wx.h>

class MainFrame : public wxFrame {
public:
    MainFrame();

    enum {
        ID_OPEN = wxID_HIGHEST + 1,
        ID_ADDMENU,
        ID_MENU1
    };

private:
    wxMenu* m_fileMenu = NULL;
    wxMenu* m_testMenu = NULL;
    wxMenuBar* m_menubar = NULL;

    wxToolBar* m_toolbar = NULL;

    void onExit(wxCommandEvent&);
    void onOpen(wxCommandEvent& ev);
    void onAddMenu(wxCommandEvent& ev);
    void onMenu1(wxCommandEvent& ev);

};