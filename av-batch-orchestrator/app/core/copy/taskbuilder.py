"""This class creates tasks for copy job.
"""
from core.config import Settings, getSettings


class TaskBuilder:
    """This class creates tasks for copy job.
    """
    source: str
    target: str
    sourceSasKey: str
    targetSasKey: str
    settings: Settings 
    
    def __init__(self, source: str, target: str, sourceSasKey: str, targetSasKey: str, settings: Settings = getSettings()):
        self.source = source
        self.target = target
        self.sourceSasKey = sourceSasKey
        self.targetSasKey = targetSasKey
        self.settings = settings
        
        
    def getRawCopyCommand(self) -> str:
        """Get the copy command for copying data to raw zone.

        Returns:
            str: Copy command for raw zone
        """
        return f"azcopy copy \"{self.settings.LANDING_ZONE_SA_URL}/{self.source}/*{self.sourceSasKey}\" \"{self.settings.RAW_ZONE_SA_URL}/{self.target}/{self.targetSasKey}\" --s2s-preserve-access-tier=false --include-directory-stub=false --recursive --log-level=INFO;"
    
    def getArchiveCopyCommand(self) -> str:
        """Get the copy command for copying data to archive zone.

        Returns:
            str: Copy command for archive zone
        """
        return f"azcopy copy \"{self.settings.LANDING_ZONE_SA_URL}/{self.source}/{self.sourceSasKey}\" \"{self.settings.ARCHIVE_ZONE_SA_URL}/{self.target}/{self.targetSasKey}\" --s2s-preserve-access-tier=false --include-directory-stub=false --recursive --log-level=INFO;"    

    def getRemoveLandingDataCommand(self) -> str:
        """Get the command for removing data from landing zone.

        Returns:
            str: Removal command for landing zone
        """
        return f"azcopy rm \"{self.settings.ARCHIVE_ZONE_SA_URL}/{self.source}/{self.sourceSasKey}\" --recursive=true;"        
        